import re
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.income import Income
from app.models.expense import Expense
from app.services.analytics_service import get_dashboard_summary, get_category_breakdown
from app.services.financial_knowledge import KNOWLEDGE_BASE


def normalize_text(text: str) -> str:
    """Lowercase and clean text for intent and keyword matching."""
    return re.sub(r"[^\w\s]", " ", text.lower()).strip()


def check_personal_finance_intent(query_clean: str) -> Optional[str]:
    """Detects if user is asking about their personal financial records."""
    patterns = {
        "spending_analysis": [
            "my spending", "analyze my", "my budget", "my expense", "my expenses",
            "how am i doing", "review my", "how much did i spend", "where does my money go",
            "spending habits", "financial health", "my cashflow"
        ],
        "save_more": [
            "save more", "how can i save", "increase my savings", "how to save more",
            "ways to save", "reduce expenses", "cut costs", "save money"
        ],
        "savings_rate": [
            "savings rate", "my savings", "how much did i save", "saving percentage"
        ],
        "category_specific": [
            "food", "transport", "education", "entertainment", "shopping", "bills", "healthcare"
        ]
    }

    if any(p in query_clean for p in patterns["spending_analysis"]):
        return "spending_analysis"
    if any(p in query_clean for p in patterns["save_more"]):
        return "save_more"
    if any(p in query_clean for p in patterns["savings_rate"]):
        return "savings_rate"
    
    # Check if asking specifically about a category in their spending (e.g., "is my food expense high?")
    if any(word in query_clean for word in ["my", "high", "too much", "spent on"]):
        for cat in patterns["category_specific"]:
            if cat in query_clean:
                return f"category_{cat}"

    return None


def generate_personal_analysis(intent: str, db: Session, current_user: User, raw_query: str) -> str:
    """Generates personalized insights directly computed from user's database records."""
    summary = get_dashboard_summary(db, current_user)
    breakdown = get_category_breakdown(db, current_user)
    total_inc = summary["total_income"]
    total_exp = summary["total_expenses"]
    savings = summary["savings"]
    savings_rate = round((savings / total_inc * 100), 1) if total_inc > 0 else 0.0

    # If no records exist yet
    if total_inc == 0 and total_exp == 0:
        return (
            "### 📊 Your Financial Snapshot\n\n"
            "You haven't recorded any income or expenses in your account yet!\n\n"
            "**Recommended First Steps:**\n"
            "1. Head to the **Income** tab and record your monthly earnings or student allowance.\n"
            "2. Head to the **Expenses** tab and log your daily expenditures (food, commute, rent, subscriptions).\n"
            "3. Once recorded, I can perform a personalized breakdown of your cashflow, highlight spending leaks, "
            "and suggest concrete ways to optimize your savings rate."
        )

    # Specific Category Query (e.g. "Is my food expense high?")
    if intent.startswith("category_"):
        cat_name = intent.replace("category_", "").capitalize()
        cat_record = next((item for item in breakdown if item["category"].lower() == cat_name.lower()), None)

        if not cat_record:
            return (
                f"### 🔍 Analysis for **{cat_name}**\n\n"
                f"You currently have no recorded expenses in the **{cat_name}** category.\n\n"
                f"- **Total Recorded Expenses**: ₹{total_exp:,.2f}\n"
                f"If you had {cat_name.lower()} expenses recently, make sure to add them on the **Expenses** page so we can monitor trends!"
            )

        cat_amount = cat_record["amount"]
        cat_pct = cat_record["percentage"]
        income_pct = round((cat_amount / total_inc * 100), 1) if total_inc > 0 else 0

        verdict = ""
        if income_pct > 25:
            verdict = "⚠️ **Elevated**: This category accounts for more than a quarter of your total recorded income."
        elif income_pct > 15:
            verdict = "⚖️ **Moderate**: This is within a typical lifestyle range, but worth watching for small recurring leaks."
        else:
            verdict = "✅ **Healthy**: This category is well-contained relative to your overall financial inflow."

        return (
            f"### 🔍 Category Evaluation: **{cat_name}**\n\n"
            f"- **Amount Spent**: ₹{cat_amount:,.2f}\n"
            f"- **Share of Total Expenses**: {cat_pct}%\n"
            f"- **Share of Total Income**: {income_pct}%\n\n"
            f"{verdict}\n\n"
            f"**Mentor Tips for {cat_name}:**\n"
            f"- Under the standard 50/30/20 budgeting rule, non-essential leisure/wants should stay under 30%, "
            f"while essential living costs should stay within 50%.\n"
            f"- Try setting a fixed weekly allowance for {cat_name.lower()} to prevent month-end overspending."
        )

    # General Spending Analysis or Saving More
    top_cats_text = ""
    for idx, item in enumerate(breakdown[:3], 1):
        top_cats_text += f"{idx}. **{item['category']}**: ₹{item['amount']:,.2f} ({item['percentage']}% of expenses)\n"

    status_badge = "✅ Positive Surplus" if savings >= 0 else "🚨 Budget Deficit"

    return (
        f"### 📊 Personalized Financial Health Diagnostic\n\n"
        f"- **Total Recorded Income**: ₹{total_inc:,.2f}\n"
        f"- **Total Recorded Expenses**: ₹{total_exp:,.2f}\n"
        f"- **Net Savings**: ₹{savings:,.2f} ({status_badge})\n"
        f"- **Savings Rate**: {savings_rate}% *(Target benchmark: 20%+)*\n\n"
        f"#### Top Outflow Categories:\n"
        f"{top_cats_text if top_cats_text else 'No category breakdown available.'}\n"
        f"#### Actionable Guidance:\n"
        f"1. **Audit Top Outflows**: Look at your #{breakdown[0]['category'] if breakdown else 'primary'} expenses. Trimming even 10-15% can boost your net surplus.\n"
        f"2. **Automate the 20% Rule**: With your income of ₹{total_inc:,.2f}, aim to route at least ₹{round(total_inc * 0.20):,.2f} into savings or index SIPs the day your income arrives.\n"
        f"3. **Emergency Cushion**: Ensure you build 3-6 months of living expenses (approx. ₹{round(total_exp * 3):,.2f} to ₹{round(total_exp * 6):,.2f}) in a high-yield savings or liquid fund."
    )


def match_knowledge_base(query_clean: str) -> Optional[Dict[str, Any]]:
    """Finds the best matching financial concept from curated knowledge base."""
    best_match = None
    max_score = 0

    for key, data in KNOWLEDGE_BASE.items():
        score = 0
        for kw in data["keywords"]:
            # Exact phrase match gives high score
            if kw in query_clean:
                score += len(kw.split()) * 3
            # Individual word match
            else:
                words = kw.split()
                if all(w in query_clean for w in words):
                    score += len(words) * 2

        if score > max_score:
            max_score = score
            best_match = data

    return best_match if max_score >= 2 else None


def format_knowledge_response(data: Dict[str, Any]) -> str:
    """Formats a knowledge entry into a clean, educational markdown response."""
    details_md = "\n".join([f"- {item}" for item in data.get("details", [])])
    categories_md = "\n".join([f"- {cat}" for cat in data.get("categories", [])])

    res = (
        f"### 💡 Understanding {data['title']}\n\n"
        f"{data['summary']}\n\n"
        f"#### Key Concepts & Principles:\n"
        f"{details_md}\n\n"
    )

    if categories_md:
        res += f"#### Types & Classifications:\n{categories_md}\n\n"

    if data.get("example"):
        res += f"#### Practical Real-World Example:\n> {data['example']}\n\n"

    res += "*Educational Note: Always evaluate your risk tolerance and investment time horizon before committing capital.*"
    return res


def generate_fallback_financial_advice(raw_query: str) -> str:
    """Structured response for general financial questions not matched by a specific topic."""
    return (
        f"### 🧭 AI Financial Mentor Guidance\n\n"
        f"Thank you for asking about: *\"{raw_query.strip()}\"*\n\n"
        f"Here are core personal finance rules that apply directly to your journey:\n\n"
        f"1. **The 50/30/20 Rule**: Allocate 50% of your earnings to essential Needs, 30% to discretionary Wants, and at least 20% to Savings and Investments.\n"
        f"2. **Emergency Cushion First**: Maintain 3 to 6 months of living expenses in an easily accessible liquid account before investing in equities or volatile assets.\n"
        f"3. **Harness Compounding via SIP**: Investing consistently every month in low-cost index funds or mutual funds averages market volatility and turns time into exponential wealth.\n"
        f"4. **Control High-Interest Liabilities**: Eliminate credit card balances and short-term personal loans first, as high interest works aggressively against compounding.\n\n"
        f"💡 *You can ask me specific questions like:*\n"
        f"- *\"What are mutual funds?\"*\n"
        f"- *\"How does a SIP work?\"*\n"
        f"- *\"Explain the rule of 72 and compound interest\"*\n"
        f"- *\"Analyze my spending this month\"*\n"
        f"- *\"How to improve my credit score?\"*"
    )


def process_financial_query(
    user_message: str,
    db: Session,
    current_user: User
) -> str:
    """Main intelligent engine that parses queries and generates dynamic responses."""
    cleaned = normalize_text(user_message)

    # 1. Check for Greetings
    greetings = ["hi", "hello", "hey", "good morning", "good evening", "namaste", "who are you"]
    if any(cleaned == g or cleaned.startswith(f"{g} ") for g in greetings):
        return (
            f"Hello {current_user.name}! 👋 I am your **AI Financial Mentor**.\n\n"
            f"I can help you:\n"
            f"- **Learn financial concepts**: Mutual funds, SIPs, Compound interest, Emergency funds, Credit scores, Stocks, Taxes.\n"
            f"- **Analyze your real finances**: Ask me *\"How is my spending?\"* or *\"Is my food expense high?\"* to inspect your recorded cashflow.\n"
            f"- **Build wealth habits**: Smart budgeting strategies and debt reduction methods.\n\n"
            f"What would you like to explore today?"
        )

    # 2. Check for Personal Finances / Spending Intent
    personal_intent = check_personal_finance_intent(cleaned)
    if personal_intent:
        return generate_personal_analysis(personal_intent, db, current_user, user_message)

    # 3. Match against Curated Financial Knowledge Base
    matched_topic = match_knowledge_base(cleaned)
    if matched_topic:
        return format_knowledge_response(matched_topic)

    # 4. Fallback structured guidance
    return generate_fallback_financial_advice(user_message)
