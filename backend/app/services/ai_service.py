import logging
from typing import List, Optional
import httpx
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
from app.models.chat_history import ChatHistory
from app.models.user import User
from app.services.analytics_service import get_dashboard_summary, get_category_breakdown
from app.services.financial_ai_engine import process_financial_query

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are "AI Financial Mentor", an empathetic, knowledgeable, and responsible educational financial guide.
Your purpose is to help users learn about personal finance, budgeting, saving, investing principles, and smart money management.

IMPORTANT RULES & BOUNDARIES:
1. You are an educational mentor, NOT a licensed financial advisor or certified financial planner.
2. Provide general educational guidance. Do not offer formal, regulated financial or legal advice.
3. Never promise or guarantee specific investment returns (e.g., never say "you will make 15% guaranteed"). Emphasize that all investments carry risk and returns fluctuate.
4. Promote responsible financial habits: building an emergency fund (3-6 months of expenses), tracking spending, following budgeting rules (such as 50/30/20), systematic investment plans (SIP), and debt reduction.
5. If the user asks about their spending or saving, use their aggregated summary provided below to give constructive, actionable observations.
6. Keep answers structured, friendly, concise, and easy for a student or beginner to understand. Use formatting like bullet points when helpful.
7. Always clarify assumptions and encourage consulting qualified professionals for binding financial decisions.
"""


def get_financial_context(db: Session, current_user: User) -> str:
    """Generates an aggregated, safe financial snapshot without exposing PII."""
    try:
        summary = get_dashboard_summary(db, current_user)
        breakdown = get_category_breakdown(db, current_user)

        top_cats = ", ".join(
            [f"{item['category']}: ₹{item['amount']:,.2f} ({item['percentage']}%)" for item in breakdown[:4]]
        ) or "None recorded"

        context = (
            f"\n[User Financial Snapshot (Aggregated for Context)]\n"
            f"- Total Recorded Income: ₹{summary['total_income']:,.2f}\n"
            f"- Total Recorded Expenses: ₹{summary['total_expenses']:,.2f}\n"
            f"- Net Savings: ₹{summary['savings']:,.2f}\n"
            f"- Top Expense Categories: {top_cats}\n"
        )
        return context
    except Exception as e:
        logger.warning(f"Could not generate financial context: {e}")
        return ""


def call_llm(user_message: str, financial_context: str) -> Optional[str]:
    """Calls the OpenAI or compatible API if configured."""
    if not OPENAI_API_KEY:
        return None

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    system_content = SYSTEM_PROMPT
    if financial_context:
        system_content += f"\n{financial_context}"

    payload = {
        "model": OPENAI_MODEL or "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.7,
        "max_tokens": 800,
    }

    url = f"{OPENAI_BASE_URL.rstrip('/')}/chat/completions"

    try:
        with httpx.Client(timeout=20.0) as client:
            resp = client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"LLM API returned status {resp.status_code}: {resp.text}")
                return None
    except Exception as exc:
        logger.error(f"Error calling LLM: {exc}")
        return None


def chat_with_mentor(
    message: str,
    db: Session,
    current_user: User
) -> ChatHistory:
    financial_context = get_financial_context(db, current_user)
    
    # 1. Try LLM API first if key is configured
    ai_reply = call_llm(message, financial_context)

    # 2. If no API key or API call failed, use the intelligent Financial Knowledge & Query Engine
    if not ai_reply:
        ai_reply = process_financial_query(message, db, current_user)

    # Persist interaction to database
    history_entry = ChatHistory(
        user_id=current_user.id,
        user_message=message,
        ai_response=ai_reply,
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)

    return history_entry


def get_user_chat_history(
    db: Session,
    current_user: User
) -> List[ChatHistory]:
    return (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == current_user.id)
        .order_by(ChatHistory.created_at.desc())
        .all()
    )


def delete_chat_history_item(
    chat_id: int,
    db: Session,
    current_user: User
) -> dict:
    entry = (
        db.query(ChatHistory)
        .filter(
            ChatHistory.id == chat_id,
            ChatHistory.user_id == current_user.id
        )
        .first()
    )
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat history item not found"
        )
    db.delete(entry)
    db.commit()
    return {"message": "Chat record deleted successfully"}
