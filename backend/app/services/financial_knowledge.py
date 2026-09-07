"""Comprehensive curated financial knowledge base for AI Financial Mentor.

Contains domain knowledge trained on authoritative personal finance principles,
SEBI/RBI investor education standards, and Investopedia concepts.
"""

KNOWLEDGE_BASE = {
    "mutual_funds": {
        "title": "Mutual Funds",
        "keywords": [
            "mutual fund", "mutual funds", "mf", "mfs", "amc", "nav",
            "expense ratio", "equity fund", "debt fund", "hybrid fund",
            "index fund", "elss", "direct plan", "regular plan"
        ],
        "summary": (
            "A **Mutual Fund** is an investment vehicle where money pooled from thousands of individual "
            "investors is professionally managed by an Asset Management Company (AMC) to invest in a "
            "diversified basket of securities such as equities (stocks), debt (bonds), or gold."
        ),
        "details": [
            "**Instant Diversification**: Buying one mutual fund unit gives you exposure to 40-100+ different companies, spreading and minimizing single-stock risk.",
            "**Professional Management**: Qualified fund managers and research analysts handle stock picking, portfolio balancing, and asset allocation.",
            "**Liquidity**: Open-ended funds permit redeeming (selling) your units at any time at the prevailing Net Asset Value (NAV).",
            "**Low Entry Barrier**: You can start investing with as little as ₹500/month via Systematic Investment Plans (SIP).",
            "**Expense Ratio**: The annual management fee charged by the AMC (typically 0.1% to 1.5%). Lower expense ratios leave more compounding growth in your pocket.",
            "**Direct vs Regular Plans**: Always prefer **Direct Plans** (no distributor commission), which yield 0.5% - 1.5% higher annual returns than Regular Plans over long horizons."
        ],
        "categories": [
            "**Equity Funds**: High risk, high long-term growth potential (Large-Cap, Mid-Cap, Small-Cap, Multi-Cap). Recommended horizon: 5+ years.",
            "**Debt Funds**: Lower risk, stable returns investing in government bonds, treasury bills, and corporate debt. Good for short to medium-term goals.",
            "**Hybrid Funds**: Balanced mix of equities and debt to provide both growth and downside protection.",
            "**Index Funds / ETFs**: Passively track market indices (like Nifty 50 or S&P 500) with ultra-low costs and zero human bias.",
            "**ELSS (Tax Saving)**: Equity Linked Savings Scheme with a 3-year lock-in offering tax deductions under Section 80C."
        ],
        "example": "Instead of researching and buying 50 separate companies with lakhs of rupees, an investor can put ₹1,000 in a Nifty 50 Index Mutual Fund and instantly own a proportional share in India's top 50 blue-chip enterprises."
    },

    "sip": {
        "title": "Systematic Investment Plan (SIP)",
        "keywords": [
            "sip", "systematic investment plan", "systematic investment", "monthly investment",
            "lumpsum vs sip", "sip vs lumpsum", "step up sip", "dollar cost averaging",
            "rupee cost averaging"
        ],
        "summary": (
            "A **Systematic Investment Plan (SIP)** is a disciplined investing strategy where a fixed sum of money "
            "is automatically debited from your bank account at periodic intervals (usually monthly) and invested into a selected mutual fund."
        ),
        "details": [
            "**Rupee Cost Averaging**: When the market drops, your fixed installment automatically buys *more* fund units; when the market rises, it buys *fewer* units. This lowers your average purchase price over time without market timing anxiety.",
            "**Power of Compounding**: Regular monthly contributions compounded over 10-25 years produce exponential corpus expansion.",
            "**Disciplined & Automated**: Removes human emotion (fear and greed) from investing by automating wealth accumulation on payday.",
            "**Step-up SIP**: Increasing your SIP contribution by 10% annually in step with salary increments can double your ultimate retirement corpus."
        ],
        "categories": [
            "**SIP vs Lumpsum**: Lumpsum works best when markets are severely discounted or when you receive a bonus; SIP is ideal for salaried earners and mitigates volatility risks.",
            "**Frequency**: Monthly is standard and optimal, though weekly and quarterly options exist."
        ],
        "example": "A monthly SIP of ₹5,000 for 15 years at an expected 12% annual return requires total contributions of ₹9,00,000 and yields a future corpus of approximately ₹25,22,880 (gaining ₹16.2 Lakhs in compounding profit)."
    },

    "compound_interest": {
        "title": "Compound Interest & The Rule of 72",
        "keywords": [
            "compound interest", "compounding", "power of compounding", "rule of 72",
            "exponential growth", "interest on interest"
        ],
        "summary": (
            "**Compound Interest** is the addition of earned interest or investment gains back to the initial principal, "
            "so that future returns are earned not just on your initial capital, but on accumulated prior returns as well."
        ),
        "details": [
            "**Formula**: A = P(1 + r/n)^(nt), where P is principal, r is annual rate of return, n is compounding frequency, and t is time in years.",
            "**Time is the Ultimate Multiplier**: The real exponential surge of compounding begins after year 7-10. An investor who starts at age 22 often accumulates twice as much wealth by age 50 as someone who starts at 32 with double the monthly capital.",
            "**Rule of 72**: A fast mental calculation to determine how many years it takes to double your capital. Divide 72 by the annual rate of return (e.g. 72 ÷ 12% = 6 years to double)."
        ],
        "categories": [
            "**Linear Growth (Simple Interest)**: You only earn returns on your original deposit.",
            "**Exponential Growth (Compound Interest)**: Your money snowball-effects over time."
        ],
        "example": "Investing ₹1,00,000 once at 12% annual return doubles to ₹2,00,000 in ~6 years, ₹4,00,000 in ~12 years, ₹8,00,000 in ~18 years, and over ₹16,00,000 in ~24 years without adding another rupee."
    },

    "budgeting": {
        "title": "Budgeting & The 50/30/20 Rule",
        "keywords": [
            "budget", "budgeting", "50/30/20", "50 30 20", "how to budget", "budget rule",
            "zero based budget", "envelope method", "cut expenses", "manage cashflow"
        ],
        "summary": (
            "**Budgeting** is the deliberate process of designing a spending roadmap for your income. "
            "A budget does not constrain your freedom; it gives every rupee a distinct purpose so you spend intentionally without guilt or debt."
        ),
        "details": [
            "**50% Needs**: Essential survival expenses that cannot be easily skipped—housing rent/mortgage, basic groceries, electricity/water utilities, healthcare, and mandatory transportation.",
            "**30% Wants**: Lifestyle choices and discretionary pleasures—dining out, cinema, subscriptions, shopping, vacations, and gadgets.",
            "**20% Savings & Debt Reduction**: Building an emergency fund, starting SIP investments, PPF, and aggressively prepaying high-interest liabilities.",
            "**Zero-Based Budgeting**: Income minus all expenditures, investments, and savings equals zero at the start of each month."
        ],
        "categories": [
            "**Pay Yourself First**: Transfer your 20%+ savings into investments immediately upon salary credit before spending on wants.",
            "**Subscription Audit**: Cancel unused gym memberships, streaming services, or software trials that quietly drain cashflow."
        ],
        "example": "If your take-home pay is ₹40,000/month: reserve ₹20,000 (50%) for living necessities, cap leisure activities at ₹12,000 (30%), and channel ₹8,000 (20%) directly into emergency savings and index mutual funds."
    },

    "emergency_fund": {
        "title": "Emergency Fund",
        "keywords": [
            "emergency fund", "emergency money", "safety net", "rainy day fund",
            "financial buffer", "unforeseen expenses", "job loss fund"
        ],
        "summary": (
            "An **Emergency Fund** is a readily accessible cash reserve created strictly for unexpected financial crises, "
            "such as sudden job transitions, critical medical emergencies, or urgent vehicle/home breakdowns."
        ),
        "details": [
            "**Optimal Size**: 3 to 6 months of mandatory living expenses (Needs). Freelancers or individuals with volatile income should target 6 to 9 months.",
            "**Capital Preservation Over Yield**: Never gamble emergency funds in stocks, crypto, or locked illiquid schemes. The objective is safety and instant liquidity.",
            "**Where to Park It**: Split between a high-yield sweep-in savings bank account and an ultra-safe Liquid or Overnight Mutual Fund.",
            "**Strict Rule**: Spending from this fund is permitted only for genuine non-negotiable emergencies. If tapped, replenishing it takes priority over all other investments."
        ],
        "categories": [
            "**Tier 1**: 1 month of expenses in a primary savings account (accessible via ATM 24/7).",
            "**Tier 2**: 3-5 months of expenses in Liquid Debt Funds or sweep-in fixed deposits offering instant T+1 redemption."
        ],
        "example": "If your mandatory survival cost is ₹25,000/month, accumulate an emergency reserve of ₹75,000 to ₹1,50,000 before initiating aggressive equity market investments."
    },

    "credit_score": {
        "title": "Credit Score & CIBIL",
        "keywords": [
            "credit score", "cibil", "cibil score", "credit rating", "credit card",
            "improve credit score", "credit utilization", "credit limit"
        ],
        "summary": (
            "A **Credit Score** (such as CIBIL, Experian, or Equifax, ranging from 300 to 900) is a numerical indicator "
            "of your creditworthiness and repayment dependability, assessed by financial institutions before approving loans or credit cards."
        ),
        "details": [
            "**Payment History (35% impact)**: Always pay 100% of your credit card bills on or before the due date. Never pay just the 'Minimum Amount Due', which incurs 36-45% annualized interest.",
            "**Credit Utilization Ratio (30% impact)**: Keep your credit card spending below 30% of your total assigned credit limit.",
            "**Credit Age (15% impact)**: Maintain older credit cards open; a long positive track record elevates your creditworthiness.",
            "**Credit Mix & Enquiries (20% impact)**: Avoid applying for multiple credit cards or personal loans within short intervals, which triggers hard inquiries.",
            "**Prime Score Target**: A score of 750 or higher grants you the fastest approvals and the lowest competitive interest rates on home and vehicle financing."
        ],
        "categories": [
            "**Excellent**: 780 - 900",
            "**Good**: 720 - 779",
            "**Average / Fair**: 650 - 719",
            "**Poor**: Below 650"
        ],
        "example": "If your credit card limit is ₹1,00,000, aim to keep your statement balance under ₹30,000 each billing cycle to maintain an optimal Credit Utilization Ratio."
    },

    "stocks": {
        "title": "Stocks & Equity Investing",
        "keywords": [
            "stock", "stocks", "shares", "share market", "equity", "stock market",
            "nifty", "sensex", "trading", "dividends", "blue chip", "multibagger"
        ],
        "summary": (
            "A **Stock** (or share) represents fractional equity ownership in a corporation. "
            "When you own a stock, you participate in the company's business expansion, future earnings, and dividend distributions."
        ),
        "details": [
            "**Investing vs Trading**: Long-term investing relies on company fundamentals and business compounding over years; short-term day trading involves market speculation and exhibits high capital loss rates.",
            "**Two Sources of Returns**: Capital appreciation (rising share price) and dividend payouts (profit sharing).",
            "**Diversification Rule**: Never stake all your savings on a single company. Beginners should establish core holdings in broad Index Funds or reputable Blue-Chip leaders.",
            "**Volatility is Normal**: Equities swing in the short run based on economic news, but historically outperform inflation and fixed income over multi-year horizons."
        ],
        "categories": [
            "**Large-Cap (Blue-Chip)**: Well-established market leaders with stable balance sheets and lower volatility.",
            "**Mid-Cap**: Growing businesses offering higher upside with moderate volatility.",
            "**Small-Cap**: High-growth emerging firms with elevated volatility and failure risk."
        ],
        "example": "Owning shares of an established consumer goods company means every time people purchase everyday necessities from that brand, you share in the corporate profitability as an equity holder."
    },

    "debt_management": {
        "title": "Debt Management & Payoff Strategies",
        "keywords": [
            "debt", "loans", "pay off debt", "credit card debt", "personal loan",
            "avalanche", "snowball", "debt avalanche", "debt snowball", "interest rate"
        ],
        "summary": (
            "**Debt Management** is the strategic elimination of borrowed liabilities to free up monthly cashflow "
            "and eliminate punitive compound interest charges working against you."
        ),
        "details": [
            "**Good Debt vs Bad Debt**: Good debt funds appreciating assets or human capital (like a prudent home mortgage or student education); bad debt finances depreciating consumer goods at predatory rates (credit cards, personal loans).",
            "**Debt Avalanche Method (Mathematically Optimal)**: List all debts by interest rate and funnel all extra money to the highest interest rate first (e.g. 40% credit cards) while paying minimums on others.",
            "**Debt Snowball Method (Psychologically Rewarding)**: Pay off the smallest debt balance first to celebrate quick psychological wins, then roll that payment into the next smallest balance.",
            "**Avoid Loan Traps**: Stay away from unregulated payday apps, zero-cost EMI traps, and high-interest borrowing for lifestyle upgrades."
        ],
        "categories": [
            "**Highest Priority**: Credit cards (36-48% APR) & payday loans.",
            "**Medium Priority**: Unsecured personal loans (12-18% APR).",
            "**Manageable Priority**: Home loans (8-9% APR with tax deductions)."
        ],
        "example": "If carrying a ₹20,000 credit card balance at 42% interest and a ₹50,000 bike loan at 11%, directing surplus cash to eliminate the credit card first saves thousands in annual interest."
    },

    "inflation": {
        "title": "Inflation & Purchasing Power",
        "keywords": [
            "inflation", "purchasing power", "real return", "nominal return",
            "price rise", "cost of living"
        ],
        "summary": (
            "**Inflation** is the gradual, persistent rise in the price of goods and services over time, "
            "which diminishes the purchasing power of your money."
        ),
        "details": [
            "**The Silent Wealth Destroyer**: If inflation runs at 6% annually, an item costing ₹100 today will cost ~₹180 in 10 years.",
            "**Nominal vs Real Return**: Real Return = Nominal Return minus Inflation. If a savings account yields 3.5% while inflation is 6%, you are experiencing a -2.5% real loss in purchasing power each year.",
            "**Beating Inflation**: Equities and equity mutual funds are historically the primary asset class delivering inflation-beating real returns (10-14% nominal vs 5-6% inflation)."
        ],
        "categories": [
            "**Headline Inflation**: Broad price movement across goods and services.",
            "**Core Inflation**: Excludes volatile food and fuel costs to show baseline economic trends."
        ],
        "example": "Keeping ₹10,000 in physical cash under a mattress guarantees that 10 years later you will only be able to purchase what ₹5,500 buys today at historical inflation rates."
    },

    "taxes_and_saving": {
        "title": "Tax Planning & Section 80C",
        "keywords": [
            "tax", "taxes", "tax saving", "80c", "section 80c", "elss", "ppf",
            "nps", "old regime", "new regime", "tax deduction"
        ],
        "summary": (
            "**Tax Planning** involves structuring your finances and investments legally to optimize deductions, "
            "lower your overall tax liability, and increase your net investable savings."
        ),
        "details": [
            "**Section 80C**: Allows deductions up to ₹1,50,000 annually from gross total income in the Old Tax Regime.",
            "**Eligible 80C Instruments**: ELSS Mutual Funds (shortest lock-in of 3 years + equity growth), Public Provident Fund (PPF - 15-year sovereign safe), EPF, and Term Insurance premiums.",
            "**National Pension System (NPS)**: Offers an additional exclusive deduction of up to ₹50,000 under Section 80CCD(1B) for retirement corpus building.",
            "**Old vs New Tax Regime**: New Regime features simplified lower slab rates but limits deductions; compare both annually based on your specific deductions."
        ],
        "categories": [
            "**ELSS**: Highest long-term return potential with tax savings.",
            "**PPF**: Guaranteed, tax-free interest backed by the Government of India."
        ],
        "example": "An individual in the 30% tax bracket investing ₹1,50,000 into an ELSS fund under Section 80C saves ₹46,800 in direct income tax while simultaneously building long-term equity wealth."
    },

    "insurance": {
        "title": "Insurance: Term & Health Protection",
        "keywords": [
            "insurance", "term insurance", "life insurance", "health insurance",
            "mediclaim", "ulip", "endowment", "policy"
        ],
        "summary": (
            "**Insurance** is risk management, not an investment. Its singular mission is protecting your dependents "
            "and assets from catastrophic financial ruin in the event of disability, hospitalization, or untimely death."
        ),
        "details": [
            "**Pure Term Life Insurance**: The only recommended life insurance. Provides massive life cover (10-20x annual income) at low annual premiums. Pay for protection, do not combine investment with insurance.",
            "**Health Insurance (Mediclaim)**: Essential for every working individual and family. A single medical emergency or hospitalization can otherwise wipe out years of accumulated savings.",
            "**Avoid ULIPs & Endowment Policies**: Traditional policies that blend insurance with investment typically offer inadequate life cover (10x premium) and poor returns (4-6% p.a.) eaten up by opaque agent charges."
        ],
        "categories": [
            "**Term Insurance**: Buy early (in your 20s) to lock in low premiums for life.",
            "**Super Top-up Health Cover**: Inexpensive way to extend corporate or base health coverage from ₹5 Lakhs to ₹25-50 Lakhs."
        ],
        "example": "A 25-year-old non-smoker can secure a ₹1 Crore pure term insurance policy for approximately ₹800 - ₹1,000 per month, providing total peace of mind for their family."
    },

    "fd_rd": {
        "title": "Fixed Deposits (FD) & Recurring Deposits (RD)",
        "keywords": [
            "fd", "rd", "fixed deposit", "recurring deposit", "bank deposit",
            "safe investment", "guaranteed return"
        ],
        "summary": (
            "**Fixed Deposits (FD)** and **Recurring Deposits (RD)** are conservative financial products offered by banks "
            "that deliver guaranteed, predetermined interest over a designated tenure."
        ),
        "details": [
            "**Capital Safety**: Bank deposits are insured up to ₹5,00,000 per depositor per bank by DICGC (RBI subsidiary).",
            "**Predictable Cashflows**: Ideal for short-term financial goals (under 1-3 years) where capital volatility cannot be tolerated (e.g., college semester fees, upcoming vacation, wedding expenses).",
            "**Tax Inefficiency**: FD interest is fully taxable at your marginal income tax slab rate, which can drag post-tax returns below inflation for higher-income earners."
        ],
        "categories": [
            "**FD**: One-time lumpsum deposit with fixed interest payout.",
            "**RD**: Monthly recurring deposits compounding over fixed months."
        ],
        "example": "If saving for a laptop you plan to purchase in 8 months, a short-term bank FD or Recurring Deposit is far safer than investing that money in volatile equity markets."
    }
}
