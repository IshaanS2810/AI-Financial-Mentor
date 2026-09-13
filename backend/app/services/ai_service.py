import logging
from typing import List, Optional
import httpx
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL
from app.models.chat_history import ChatHistory
from app.models.user import User
from app.services.financial_profile_service import get_financial_profile
from app.services.financial_analysis_service import calculate_user_financial_analysis
from app.services.recommendation_service import generate_personalized_recommendations
from app.services.financial_ai_engine import process_financial_query

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are "AI Financial Mentor", an empathetic, knowledgeable, and responsible educational financial guide.
Your purpose is to provide general financial education and personalized educational guidance based on the user's financial information.

CRITICAL GUIDELINES & BOUNDARIES:
1. You are an educational mentor, NOT a licensed financial advisor or certified broker. Always make clear that responses are educational suggestions and not formal investment or legal advice.
2. When answering personalized questions ("Can I afford to invest?", "How much should I invest?", "Why was SIP recommended?"), use the user's provided financial summary and risk profile.
3. Never guarantee returns or claim an investment is risk-free.
4. Never instruct the user to buy a specific individual stock.
5. Emphasize sound personal finance concepts: emergency funds, savings, SIPs, diversified index mutual funds, risk management, and long-term asset allocation.
6. Clearly explain WHY a recommendation is appropriate for their specific financial situation.
7. Distinguish between:
   - Facts calculated from user data (income, expenses, savings rate)
   - Educational suggestions (exploring SIPs, trimming discretionary spending)
   - Assumptions/estimates (emergency fund coverage months based on recorded expenses)
8. If the user's financial profile or expense data is missing, gently state what is missing rather than fabricating numbers.
9. Encourage users to consult qualified professionals before making binding financial commitments.
"""


def get_financial_context(db: Session, current_user: User) -> str:
    """Generates an aggregated, safe financial snapshot including profile and recommendations."""
    try:
        analysis = calculate_user_financial_analysis(db, current_user)
        profile = get_financial_profile(db, current_user)
        recs_data = generate_personalized_recommendations(db, current_user)

        top_cats = ", ".join(
            [f"{item['category']}: ₹{item['amount']:,.2f} ({item['percentage']}%)" for item in analysis["top_categories"]]
        ) or "None recorded"

        rec_titles = "; ".join([f"[{r.priority}] {r.title}" for r in recs_data.recommendations[:4]])

        context = (
            f"\n[User Financial Profile & Calculated Summary]\n"
            f"- Average Monthly Income: ₹{analysis['monthly_income']:,.2f}\n"
            f"- Average Monthly Expenses: ₹{analysis['monthly_expenses']:,.2f}\n"
            f"- Monthly Savings/Surplus: ₹{analysis['monthly_savings']:,.2f}\n"
            f"- Savings Rate: {analysis['savings_rate']}%\n"
            f"- Investment Readiness Status: {analysis['investment_readiness']}\n"
            f"- Estimated Monthly Investment Capacity: ₹{analysis['investment_capacity']:,.2f}\n"
            f"- Recorded Emergency Fund: ₹{analysis['emergency_fund']:,.2f} (~{analysis['estimated_emergency_months']} months coverage)\n"
            f"- Risk Tolerance: {profile.risk_tolerance if profile else 'Not configured'}\n"
            f"- Investment Horizon: {profile.investment_horizon if profile else 'Not configured'}\n"
            f"- Financial Goal: {profile.financial_goal if profile else 'Not configured'}\n"
            f"- Top Expense Outflows: {top_cats}\n"
            f"- Active System Recommendations: {rec_titles}\n"
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
        "max_tokens": 900,
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
