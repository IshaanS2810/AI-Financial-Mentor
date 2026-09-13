from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.financial_profile import FinancialProfile
from app.services.financial_profile_service import get_financial_profile
from app.services.financial_analysis_service import calculate_user_financial_analysis
from app.schemas.recommendation import (
    RecommendationItem,
    FinancialSummaryData,
    InvestorProfileData,
    PersonalizedRecommendationsResponse,
)


def generate_personalized_recommendations(
    db: Session,
    current_user: User
) -> PersonalizedRecommendationsResponse:
    """Generates rule-based, educational investment recommendations tailored to user finances."""
    analysis = calculate_user_financial_analysis(db, current_user)
    profile = get_financial_profile(db, current_user)

    monthly_income = analysis["monthly_income"]
    monthly_expenses = analysis["monthly_expenses"]
    monthly_savings = analysis["monthly_savings"]
    savings_rate = analysis["savings_rate"]
    emergency_fund = analysis["emergency_fund"]
    emergency_months = analysis["estimated_emergency_months"]
    readiness = analysis["investment_readiness"]
    capacity = analysis["investment_capacity"]
    top_categories = analysis["top_categories"]

    risk_tolerance = profile.risk_tolerance if profile else "Moderate"
    investment_horizon = profile.investment_horizon if profile else "5–10 years"
    financial_goal = profile.financial_goal if profile else "Wealth creation"

    recommendations: List[RecommendationItem] = []

    # -------------------------------------------------------------
    # RULE 1: Emergency Fund Coverage
    # -------------------------------------------------------------
    if emergency_months < 3.0:
        target_buffer = max(monthly_expenses * 3, 30000)
        recommendations.append(
            RecommendationItem(
                id="rec_emergency_fund_priority",
                title="Prioritize Building an Emergency Safety Buffer",
                category="EMERGENCY_FUND",
                priority="HIGH",
                reason=(
                    f"Your recorded emergency savings (₹{emergency_fund:,.0f}) cover approximately "
                    f"{emergency_months} months of living expenses (benchmark is 3–6 months)."
                ),
                explanation=(
                    "Before increasing long-term market investments, building an emergency buffer prevents "
                    "you from having to liquidate investments during market downturns to cover unexpected expenses."
                ),
                suggested_action=(
                    f"Direct the majority of your monthly surplus (aim for at least ₹{max(monthly_savings * 0.7, 1000):,.0f}/month) "
                    f"into a high-yield savings account or liquid mutual fund until you reach ₹{target_buffer:,.0f}."
                )
            )
        )
    elif emergency_months >= 3.0 and emergency_months < 6.0:
        recommendations.append(
            RecommendationItem(
                id="rec_emergency_fund_maintain",
                title="Maintain & Gradually Bolster Emergency Reserves",
                category="EMERGENCY_FUND",
                priority="LOW",
                reason=f"Your emergency fund provides a sound {emergency_months}-month cushion.",
                explanation="Your emergency buffer is in a healthy range, giving you stability to begin investing.",
                suggested_action="Keep this reserve in an easily accessible liquid account and replenish it if tapped."
            )
        )

    # -------------------------------------------------------------
    # RULE 2: Cashflow & Monthly Deficit
    # -------------------------------------------------------------
    if monthly_savings <= 0:
        recommendations.append(
            RecommendationItem(
                id="rec_cashflow_stabilization",
                title="Stabilize Cashflow & Eliminate Monthly Deficit",
                category="INCREASE_SAVINGS",
                priority="HIGH",
                reason=(
                    f"Your monthly expenses (₹{monthly_expenses:,.0f}) equal or exceed your recorded "
                    f"monthly income (₹{monthly_income:,.0f}), resulting in a deficit of ₹{abs(monthly_savings):,.0f}."
                ),
                explanation=(
                    "Investing while running a deficit increases financial stress and may lead to debt. "
                    "Restoring a positive monthly surplus is the primary foundation of wealth building."
                ),
                suggested_action=(
                    "Review discretionary expenditures (dining, shopping, subscriptions) to bring your monthly "
                    "outgoings comfortably below your income."
                )
            )
        )
    elif savings_rate < 20.0 and monthly_income > 0:
        recommendations.append(
            RecommendationItem(
                id="rec_improve_savings_rate",
                title="Work Toward a 20%+ Savings Benchmark",
                category="INCREASE_SAVINGS",
                priority="MEDIUM",
                reason=f"Your current savings rate is {savings_rate}%, below the standard 20% target.",
                explanation=(
                    "Under the 50/30/20 framework, directing 20% of net income toward savings and investments "
                    "accelerates financial independence without sacrificing everyday living quality."
                ),
                suggested_action=(
                    f"Aim to increase your monthly savings by ₹{max(monthly_income * 0.20 - monthly_savings, 500):,.0f} "
                    "by adopting the 'Pay Yourself First' habit on payday."
                )
            )
        )

    # -------------------------------------------------------------
    # RULE 3: Discretionary Spending Inspection
    # -------------------------------------------------------------
    if top_categories and top_categories[0]["percentage"] >= 35.0:
        top_cat = top_categories[0]
        if top_cat["category"] in ["Food", "Shopping", "Entertainment", "Other"]:
            recommendations.append(
                RecommendationItem(
                    id="rec_trim_discretionary",
                    title=f"Audit Spending Outflows in {top_cat['category']}",
                    category="SPENDING",
                    priority="MEDIUM",
                    reason=(
                        f"{top_cat['category']} represents {top_cat['percentage']}% of your total expenses "
                        f"(₹{top_cat['amount']:,.0f} spent)."
                    ),
                    explanation=(
                        f"Large lifestyle concentrations in {top_cat['category'].lower()} can quietly erode "
                        "your surplus. Trimming even 10–15% in this area creates immediate investable capital."
                    ),
                    suggested_action=(
                        f"Set a weekly budget for {top_cat['category'].lower()} to potentially redirect "
                        f"₹{top_cat['amount'] * 0.15:,.0f}/month toward your investment goals."
                    )
                )
            )

    # -------------------------------------------------------------
    # RULE 4: Horizon-Aligned Investment Exploration
    # -------------------------------------------------------------
    if "less than 3 years" in investment_horizon.lower():
        recommendations.append(
            RecommendationItem(
                id="rec_short_term_capital_preservation",
                title="Focus on Capital Preservation & Liquid Options",
                category="SHORT_TERM_CONSERVATIVE",
                priority="HIGH" if readiness != "NOT_READY" else "MEDIUM",
                reason=f"Your investment horizon is short ({investment_horizon}).",
                explanation=(
                    "Equities fluctuate over short horizons (1–3 years). When capital is needed soon, "
                    "avoiding market drawdowns is far more important than chasing aggressive yields."
                ),
                suggested_action=(
                    "Explore low-volatility instruments such as Bank Fixed Deposits, Recurring Deposits, "
                    "or Ultra Short Duration Debt Funds rather than volatile stocks."
                )
            )
        )
    elif "3–5 years" in investment_horizon or "3-5" in investment_horizon:
        recommendations.append(
            RecommendationItem(
                id="rec_medium_term_hybrid",
                title="Consider Balanced & Hybrid Investment Approaches",
                category="MUTUAL_FUNDS",
                priority="MEDIUM",
                reason=f"Your stated horizon is {investment_horizon}, suited for balanced exposure.",
                explanation=(
                    "A 3–5 year timeframe permits moderate equity exposure for growth while utilizing fixed-income "
                    "assets to protect against severe market dips."
                ),
                suggested_action=(
                    "Consider learning about Conservative Hybrid or Multi-Asset Allocation mutual funds "
                    "that automatically balance equity and debt."
                )
            )
        )
    else:  # 5–10 years or More than 10 years
        if readiness in ["READY_TO_EXPLORE", "STRONG_INVESTMENT_CAPACITY"]:
            recommendations.append(
                RecommendationItem(
                    id="rec_long_term_sip_equity",
                    title="Harness Compounding with Disciplined Equity SIPs",
                    category="INVESTING_SIP",
                    priority="HIGH",
                    reason=(
                        f"You have a long-term horizon ({investment_horizon}) and an estimated monthly "
                        f"investment capacity of ~₹{capacity:,.0f}."
                    ),
                    explanation=(
                        "Over 5 to 10+ years, broad-market index funds (e.g. Nifty 50 or S&P 500) have historically "
                        "delivered inflation-beating compound returns while smoothing short-term market volatility."
                    ),
                    suggested_action=(
                        f"Consider starting an automated monthly SIP between ₹{min(capacity, 2000):,.0f} and "
                        f"₹{capacity:,.0f} in a low-cost, diversified index mutual fund."
                    )
                )
            )

    # -------------------------------------------------------------
    # RULE 5: Risk Tolerance Calibration
    # -------------------------------------------------------------
    if risk_tolerance == "Conservative" and ("5" in investment_horizon or "10" in investment_horizon):
        recommendations.append(
            RecommendationItem(
                id="rec_conservative_allocation",
                title="Structure a Balanced Portfolio to Match Conservative Comfort",
                category="DIVERSIFICATION",
                priority="MEDIUM",
                reason="You selected Conservative risk tolerance for a long-term goal.",
                explanation=(
                    "Conservative investors can mitigate volatility by combining stable government-backed instruments "
                    "(PPF, debt funds) with a modest core in large-cap index funds."
                ),
                suggested_action=(
                    "Explore a 60% debt / 40% large-cap equity mix to achieve inflation-protected growth "
                    "without experiencing stressful portfolio swings."
                )
            )
        )
    elif risk_tolerance == "Aggressive":
        recommendations.append(
            RecommendationItem(
                id="rec_aggressive_discipline",
                title="Embrace Long-Term Equity Compounding with Regular Rebalancing",
                category="LONG_TERM_EQUITY",
                priority="LOW",
                reason="You selected Aggressive risk tolerance.",
                explanation=(
                    "An aggressive stance allows you to tolerate market corrections for higher long-term potential. "
                    "However, true aggressive wealth creation relies on diversified index compounding rather than speculative trading."
                ),
                suggested_action=(
                    "Channel capital into broad-market index funds and flexi-cap funds, holding steadfastly through downturns."
                )
            )
        )

    # -------------------------------------------------------------
    # RULE 6: Near-Term Liquidity Safeguard
    # -------------------------------------------------------------
    recommendations.append(
        RecommendationItem(
            id="rec_liquidity_safeguard",
            title="Keep Near-Term Operational Cash Fully Liquid",
            category="LIQUIDITY_NEAR_TERM",
            priority="LOW",
            reason="Everyday living costs must not be tied up in volatile or locked instruments.",
            explanation=(
                "Never invest money needed for rent, utility bills, or upcoming semester fees into market-linked instruments."
            ),
            suggested_action=(
                "Keep at least 1 month of normal living expenses in your primary bank account for smooth day-to-day operations."
            )
        )
    )

    # Format Summary and Profile DTOs
    financial_summary_dto = FinancialSummaryData(
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        monthly_savings=monthly_savings,
        savings_rate=savings_rate,
        investment_capacity=capacity,
        emergency_fund=emergency_fund,
        estimated_emergency_months=emergency_months,
        investment_readiness=readiness,
        investment_readiness_explanation=analysis["investment_readiness_explanation"]
    )

    profile_dto = None
    if profile:
        profile_dto = InvestorProfileData(
            age=profile.age,
            risk_tolerance=profile.risk_tolerance,
            investment_horizon=profile.investment_horizon,
            financial_goal=profile.financial_goal,
            emergency_fund=profile.emergency_fund,
            risk_behavior=profile.risk_behavior,
        )

    return PersonalizedRecommendationsResponse(
        financial_summary=financial_summary_dto,
        profile=profile_dto,
        recommendations=recommendations
    )
