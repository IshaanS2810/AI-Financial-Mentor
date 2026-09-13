import re
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.financial_profile_service import get_financial_profile
from app.services.financial_analysis_service import calculate_user_financial_analysis
from app.services.recommendation_service import generate_personalized_recommendations
from app.services.financial_knowledge import KNOWLEDGE_BASE


def normalize_text(text: str) -> str:
    """Lowercase and clean text for intent and keyword matching."""
    return re.sub(r"[^\w\s]", " ", text.lower()).strip()


def check_personal_finance_intent(query_clean: str) -> Optional[str]:
    """Detects if user is asking about their personal financial situation or recommendations."""
    # 1. Specific personalized questions
    if any(p in query_clean for p in [
        "afford to invest", "afford investing", "ready to invest", "should i start investing",
        "can i invest", "can i start investing", "ready for investing", "am i ready to invest",
        "can i afford", "should i invest in mutual funds"
    ]):
        return "afford_investing"

    if any(p in query_clean for p in [
        "how much should i invest", "how much can i invest", "how much to invest",
        "how much of my surplus", "investment capacity", "invest every month",
        "how much monthly", "how much money can i invest"
    ]):
        return "how_much_invest"

    if any(p in query_clean for p in [
        "should i start a sip", "start sip for me", "is sip good for me", "should i do a sip",
        "should i invest in sip"
    ]):
        return "should_start_sip"

    if any(p in query_clean for p in [
        "why did you recommend", "why do you recommend", "why mutual funds for me",
        "why was this recommended", "explain my recommendation", "why recommend",
        "why this recommendation"
    ]):
        return "why_recommendation"

    if any(p in query_clean for p in [
        "emergency fund first", "focus on emergency fund", "is my emergency fund enough",
        "prioritize emergency", "emergency fund coverage", "should i focus on emergency"
    ]):
        return "emergency_fund_priority"

    if any(p in query_clean for p in [
        "what should i prioritize", "financial priorities", "what to do first",
        "next financial step", "where should i start", "what should i do first"
    ]):
        return "financial_priorities"

    if any(p in query_clean for p in [
        "am i saving enough", "is my savings rate good", "saving enough money", "enough savings"
    ]):
        return "saving_enough"

    # 2. General spending and cashflow queries
    if any(p in query_clean for p in [
        "my spending", "analyze my", "my budget", "my expense", "my expenses",
        "how am i doing", "review my", "how much did i spend", "where does my money go",
        "spending habits", "financial health", "my cashflow", "spending data", "where am i spending"
    ]):
        return "spending_analysis"

    if any(p in query_clean for p in [
        "save more", "how can i save", "increase my savings", "how to save more",
        "ways to save", "reduce expenses", "cut costs", "save money"
    ]):
        return "save_more"

    if any(p in query_clean for p in ["savings rate", "my savings", "how much did i save", "saving percentage"]):
        return "savings_rate"

    # Category-specific personal inquiries (e.g., "is my food expense high?")
    if any(word in query_clean for word in ["my", "high", "too much", "spent on"]):
        for cat in ["food", "transport", "education", "entertainment", "shopping", "bills", "healthcare"]:
            if cat in query_clean:
                return f"category_{cat}"

    return None


def generate_personal_analysis(intent: str, db: Session, current_user: User, raw_query: str) -> str:
    """Generates personalized insights and explanations directly computed from user's data and profile."""
    analysis = calculate_user_financial_analysis(db, current_user)
    profile = get_financial_profile(db, current_user)
    recs_response = generate_personalized_recommendations(db, current_user)

    total_inc = analysis["total_income"]
    total_exp = analysis["total_expenses"]
    monthly_inc = analysis["monthly_income"]
    monthly_exp = analysis["monthly_expenses"]
    monthly_savings = analysis["monthly_savings"]
    savings_rate = analysis["savings_rate"]
    emergency_fund = analysis["emergency_fund"]
    emergency_months = analysis["estimated_emergency_months"]
    readiness = analysis["investment_readiness"]
    capacity = analysis["investment_capacity"]
    top_categories = analysis["top_categories"]
    recommendations = recs_response.recommendations

    horizon = profile.investment_horizon if profile else "5–10 years (default)"
    risk_tol = profile.risk_tolerance if profile else "Moderate (default)"
    goal = profile.financial_goal if profile else "Wealth creation (default)"

    # Profile Missing Notice
    profile_missing_note = ""
    if not profile:
        profile_missing_note = (
            "\n\n*(Note: You haven't filled out your **Financial Profile** yet. "
            "Visit the **Profile** page to specify your risk tolerance, timeline, and emergency savings for even sharper guidance!)*"
        )

    # -------------------------------------------------------------
    # INTENT: "Can I afford to start investing?"
    # -------------------------------------------------------------
    if intent == "afford_investing":
        if monthly_inc <= 0:
            return (
                "### 🧭 Investment Readiness Assessment\n\n"
                "You currently have no recorded income in your account. To invest responsibly, "
                "you first need a consistent inflow of income.\n\n"
                "**Action Plan:** Log your income in the **Income** tab, then we can calculate your surplus."
            )
        if monthly_savings <= 0:
            return (
                f"### 🧭 Investment Readiness Assessment\n\n"
                f"Based on your recorded figures, you earn approximately ₹{monthly_inc:,.0f}/month and spend around "
                f"₹{monthly_exp:,.0f}/month, operating with a monthly deficit of ₹{abs(monthly_savings):,.0f}.\n\n"
                "**Current Status: NOT READY TO INVEST**\n"
                "Investing while in deficit risks running into debt or being forced to sell at a loss. "
                "Your immediate focus should be trimming discretionary outflows to establish positive cashflow."
                + profile_missing_note
            )
        if emergency_months < 3.0:
            return (
                f"### 🧭 Investment Readiness Assessment\n\n"
                f"You earn approximately ₹{monthly_inc:,.0f} and spend around ₹{monthly_exp:,.0f} per month, leaving a "
                f"healthy monthly surplus of **₹{monthly_savings:,.0f}** (Savings Rate: {savings_rate}%).\n\n"
                f"**Current Status: BUILD EMERGENCY FUND FIRST**\n"
                f"Your recorded emergency savings are ₹{emergency_fund:,.0f}, covering approximately **{emergency_months} months** "
                f"of living expenses (benchmark is 3–6 months).\n\n"
                f"**Mentor Recommendation:** Rather than committing all your surplus to long-term volatile investments, "
                f"we recommend allocating ~75% of your surplus (₹{monthly_savings * 0.75:,.0f}) toward building your safety reserve, "
                f"while exploring small starter investments (approx. ₹{capacity:,.0f}/month in a low-cost index SIP) for educational experience."
                + profile_missing_note
            )
        return (
            f"### 🧭 Investment Readiness Assessment: ✅ Ready to Invest\n\n"
            f"Great news! Your financial indicators are in a favorable position:\n"
            f"- **Monthly Inflow**: ₹{monthly_inc:,.0f}\n"
            f"- **Monthly Outflow**: ₹{monthly_exp:,.0f}\n"
            f"- **Monthly Surplus**: ₹{monthly_savings:,.0f} (Savings Rate: {savings_rate}%)\n"
            f"- **Emergency Coverage**: ~{emergency_months} months (₹{emergency_fund:,.0f})\n"
            f"- **Estimated Monthly Capacity**: ₹{capacity:,.0f}\n\n"
            f"Given your stated **{horizon}** horizon and **{risk_tol}** risk tolerance, you appear financially "
            f"ready to explore disciplined monthly investing such as broad-market index mutual funds (SIP)."
            + profile_missing_note
        )

    # -------------------------------------------------------------
    # INTENT: "How much should I invest every month?"
    # -------------------------------------------------------------
    if intent == "how_much_invest":
        if monthly_savings <= 0:
            return (
                f"### 💰 Recommended Monthly Investment Allocation\n\n"
                f"Currently, your monthly expenses (₹{monthly_exp:,.0f}) match or exceed your income (₹{monthly_inc:,.0f}). "
                "Because your monthly surplus is ₹0 or negative, you should not allocate funds to investing right now. "
                "Focus on creating a positive monthly surplus first."
            )
        return (
            f"### 💰 Recommended Monthly Investment Allocation\n\n"
            f"- **Calculated Monthly Surplus**: ₹{monthly_savings:,.0f} (Income: ₹{monthly_inc:,.0f} - Expenses: ₹{monthly_exp:,.0f})\n"
            f"- **Emergency Fund Status**: ~{emergency_months} months coverage\n"
            f"- **Suggested Investment Allocation**: **₹{capacity:,.0f} per month**\n\n"
            f"#### Why not invest all ₹{monthly_savings:,.0f}?\n"
            f"We use a conservative educational heuristic: "
            f"{'Because your emergency buffer is below 3 months, 75% of your surplus is prioritized for emergency savings, leaving 25% (₹' + f'{capacity:,.0f}) for starter investments.' if emergency_months < 3 else 'Even with an adequate safety net, keeping 20-40% of surplus liquid ensures ongoing flexibility for irregular expenses and peace of mind.'}\n\n"
            f"**Suggested Next Step:** Consider an automated monthly SIP between ₹{min(capacity, 1000):,.0f} and ₹{capacity:,.0f} on payday."
            + profile_missing_note
        )

    # -------------------------------------------------------------
    # INTENT: "Should I start a SIP?" / "Why did you recommend mutual funds/SIP?"
    # -------------------------------------------------------------
    if intent in ["should_start_sip", "why_recommendation"]:
        rec_sip = next((r for r in recommendations if "SIP" in r.title or "Hybrid" in r.title or "Mutual" in r.category or "INVESTING" in r.category), None)
        return (
            f"### 📈 Why Mutual Funds & SIP Fit Your Profile\n\n"
            f"Based on your recorded numbers and investor profile:\n"
            f"1. **Monthly Surplus**: You generate ~₹{monthly_savings:,.0f}/month, providing regular investable cashflow.\n"
            f"2. **Investment Horizon**: You indicated a **{horizon}** timeline. "
            f"{'Over 5+ years, equities historically outpace inflation through compounding while smoothing short-term market cycles.' if '5' in horizon or '10' in horizon else 'For a shorter horizon, balanced hybrid or debt mutual funds provide stability over pure equity.'}\n"
            f"3. **Risk Profile**: With a **{risk_tol}** risk tolerance, diversified index funds prevent company-specific wipeout risk compared to single stocks.\n"
            f"4. **Rupee Cost Averaging**: An automated SIP buys more units when markets dip and fewer when markets surge, removing stressful market timing.\n\n"
            f"*(Recommendation: {rec_sip.title if rec_sip else 'Explore index mutual fund SIPs'})*\n\n"
            f"*Important: This is educational guidance. Mutual fund investments are subject to market risks.*"
            + profile_missing_note
        )

    # -------------------------------------------------------------
    # INTENT: "Should I focus on my emergency fund first?"
    # -------------------------------------------------------------
    if intent == "emergency_fund_priority":
        verdict = "Yes, absolutely!" if emergency_months < 3.0 else "You already have a healthy foundation!"
        return (
            f"### 🛡️ Emergency Fund Evaluation: {verdict}\n\n"
            f"- **Recorded Emergency Savings**: ₹{emergency_fund:,.0f}\n"
            f"- **Average Monthly Expenses**: ₹{monthly_exp:,.0f}\n"
            f"- **Current Coverage**: **{emergency_months} months** (Standard guideline is 3–6 months)\n\n"
            f"{'Because your coverage is below 3 months, unexpected medical bills, car repairs, or career interruptions could force you to borrow at high interest or sell long-term investments at market lows. Making emergency savings your primary priority builds unbreakable financial resilience.' if emergency_months < 3 else 'With 3+ months of expenses saved, you have an effective shock absorber and can comfortably direct the majority of new monthly surplus toward long-term investing.'}"
            + profile_missing_note
        )

    # -------------------------------------------------------------
    # INTENT: "What should I prioritize financially?"
    # -------------------------------------------------------------
    if intent == "financial_priorities":
        recs_list_text = "\n".join([f"{idx+1}. **[{r.priority}] {r.title}**: {r.suggested_action}" for idx, r in enumerate(recommendations[:3])])
        return (
            f"### 🎯 Your Top Financial Priorities\n\n"
            f"Based on our algorithmic rule-based analysis of your records:\n\n"
            f"{recs_list_text}\n\n"
            f"**Your Current Status**: **{readiness.replace('_', ' ')}**\n"
            f"*(Visit the **Recommendations** page to view the full prioritized breakdown)*"
            + profile_missing_note
        )

    # -------------------------------------------------------------
    # INTENT: "Am I saving enough?"
    # -------------------------------------------------------------
    if intent in ["saving_enough", "savings_rate"]:
        status_text = "excellent" if savings_rate >= 30 else ("healthy" if savings_rate >= 20 else "below target")
        return (
            f"### 📊 Savings Rate Analysis\n\n"
            f"- **Monthly Income**: ₹{monthly_inc:,.0f}\n"
            f"- **Monthly Expenses**: ₹{monthly_exp:,.0f}\n"
            f"- **Net Monthly Savings**: ₹{monthly_savings:,.0f}\n"
            f"- **Savings Rate**: **{savings_rate}%** (Benchmark: 20%+)\n\n"
            f"Your current savings rate is **{status_text}**. "
            f"{'Aim to adopt the 50/30/20 rule to increase savings toward the 20% mark.' if savings_rate < 20 else 'You are meeting or exceeding standard wealth-building benchmarks! Ensure your surplus is actively working for you via index SIPs.'}"
            + profile_missing_note
        )

    # -------------------------------------------------------------
    # INTENT: Specific Category Query (e.g. "Is my food expense high?")
    # -------------------------------------------------------------
    if intent.startswith("category_"):
        cat_name = intent.replace("category_", "").capitalize()
        cat_record = next((item for item in analysis["category_breakdown"] if item["category"].lower() == cat_name.lower()), None)

        if not cat_record:
            return (
                f"### 🔍 Analysis for **{cat_name}**\n\n"
                f"You currently have no recorded expenses in the **{cat_name}** category.\n\n"
                f"- **Total Recorded Expenses**: ₹{total_exp:,.2f}\n"
                f"Log items on the **Expenses** page to monitor category trends!"
            )

        cat_amount = cat_record["amount"]
        cat_pct = cat_record["percentage"]
        income_pct = round((cat_amount / monthly_inc * 100), 1) if monthly_inc > 0 else 0

        verdict = (
            "⚠️ **Elevated**: Accounts for over 25% of your monthly income."
            if income_pct > 25
            else ("⚖️ **Moderate**: Within typical range." if income_pct > 15 else "✅ **Healthy**: Well-contained.")
        )

        return (
            f"### 🔍 Category Evaluation: **{cat_name}**\n\n"
            f"- **Amount Spent**: ₹{cat_amount:,.2f}\n"
            f"- **Share of Expenses**: {cat_pct}%\n"
            f"- **Share of Income**: {income_pct}%\n\n"
            f"{verdict}\n\n"
            f"**Mentor Tip**: Under the 50/30/20 framework, all non-essential wants combined should stay within 30% of income."
        )

    # -------------------------------------------------------------
    # INTENT: General Spending Analysis
    # -------------------------------------------------------------
    top_cats_text = ""
    for idx, item in enumerate(top_categories[:3], 1):
        top_cats_text += f"{idx}. **{item['category']}**: ₹{item['amount']:,.2f} ({item['percentage']}% of expenses)\n"

    status_badge = "✅ Positive Surplus" if monthly_savings >= 0 else "🚨 Budget Deficit"

    return (
        f"### 📊 Personalized Financial Health Diagnostic\n\n"
        f"- **Monthly Income**: ₹{monthly_inc:,.2f}\n"
        f"- **Monthly Expenses**: ₹{monthly_exp:,.2f}\n"
        f"- **Monthly Surplus**: ₹{monthly_savings:,.2f} ({status_badge})\n"
        f"- **Savings Rate**: {savings_rate}% *(Target: 20%+)*\n"
        f"- **Investment Readiness**: {readiness.replace('_', ' ')}\n"
        f"- **Estimated Monthly Investment Capacity**: ₹{capacity:,.2f}\n\n"
        f"#### Top Outflow Categories:\n"
        f"{top_cats_text if top_cats_text else 'No category breakdown available.'}\n"
        f"#### Key Observations:\n"
        f"1. **Emergency Cushion**: You have ~{emergency_months} months of expense reserves.\n"
        f"2. **Next Step**: {recommendations[0].title if recommendations else 'Review your monthly cashflow on the Recommendations page.'}"
        + profile_missing_note
    )


def match_knowledge_base(query_clean: str) -> Optional[Dict[str, Any]]:
    """Finds the best matching financial concept from curated knowledge base."""
    best_match = None
    max_score = 0

    for key, data in KNOWLEDGE_BASE.items():
        score = 0
        for kw in data["keywords"]:
            if kw in query_clean:
                score += len(kw.split()) * 3
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
        f"3. **Harness Compounding via SIP**: Investing consistently every month in low-cost index funds averages market volatility and turns time into exponential wealth.\n"
        f"4. **Control High-Interest Liabilities**: Eliminate credit card balances and short-term personal loans first, as high interest works aggressively against compounding.\n\n"
        f"💡 *You can ask me questions like:*\n"
        f"- *\"What are mutual funds?\"* (Generic concept)\n"
        f"- *\"Can I afford to start investing?\"* (Personalized)\n"
        f"- *\"How much should I invest every month?\"* (Personalized)\n"
        f"- *\"Why did you recommend SIP for me?\"* (Personalized)\n"
        f"- *\"Should I focus on my emergency fund first?\"* (Personalized)"
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
            f"- **Personalized Insights**: Ask *\"Can I afford to invest?\"*, *\"How much should I invest?\"*, or *\"Why did you recommend mutual funds for me?\"*\n"
            f"- **Analyze Cashflow**: Ask *\"Analyze my spending\"* or *\"Is my food expense high?\"*\n"
            f"- **Learn Concepts**: Ask *\"What are mutual funds?\"*, *\"What is compound interest?\"*, or *\"What is an emergency fund?\"*\n\n"
            f"How can I assist your financial journey today?"
        )

    # 2. Check for Personalized Questions first (takes user data into account)
    personal_intent = check_personal_finance_intent(cleaned)
    if personal_intent:
        return generate_personal_analysis(personal_intent, db, current_user, user_message)

    # 3. Match against Curated Financial Knowledge Base (generic concepts)
    matched_topic = match_knowledge_base(cleaned)
    if matched_topic:
        return format_knowledge_response(matched_topic)

    # 4. Fallback structured guidance
    return generate_fallback_financial_advice(user_message)
