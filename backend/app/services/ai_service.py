import logging
from typing import List, Optional
import httpx
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
from app.models.chat_history import ChatHistory
from app.models.user import User
from app.services.analytics_service import get_dashboard_summary, get_category_breakdown

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


def call_llm(user_message: str, financial_context: str) -> str:
    """Calls the OpenAI or compatible API using httpx."""
    if not OPENAI_API_KEY:
        # Fallback educational response if API key is not configured in .env
        return (
            "*(Note: OPENAI_API_KEY is not configured in backend/.env. Running in offline educational mode.)*\n\n"
            "Hello! I am your AI Financial Mentor. To enable full dynamic AI responses, please add your "
            "`OPENAI_API_KEY` to the `.env` file.\n\n"
            "In the meantime, here is some key financial guidance:\n"
            "- **Budgeting**: Consider using the 50/30/20 framework (50% Needs, 30% Wants, 20% Savings/Investments).\n"
            "- **Emergency Fund**: Aim to keep 3 to 6 months of essential living expenses in a liquid savings account or liquid mutual fund.\n"
            "- **Compound Interest & SIP**: Starting early with Systematic Investment Plans allows compounding to work in your favor over long horizons.\n\n"
            "*Disclaimer: This information is strictly educational and does not constitute certified financial advice.*"
        )

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
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"LLM API returned status {resp.status_code}: {resp.text}")
                return (
                    f"I encountered an error contacting the AI service (Status {resp.status_code}). "
                    "Please verify your API key and connection in `.env`. "
                    "Remember that financial planning starts with keeping an emergency fund and tracking your daily expenses!"
                )
    except Exception as exc:
        logger.error(f"Error calling LLM: {exc}")
        return (
            "I could not connect to the AI service at this moment. "
            f"Error details: {str(exc)}. Please check your internet connection and API key in backend/.env."
        )


def chat_with_mentor(
    message: str,
    db: Session,
    current_user: User
) -> ChatHistory:
    financial_context = get_financial_context(db, current_user)
    ai_reply = call_llm(message, financial_context)

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
