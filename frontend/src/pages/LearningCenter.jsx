import React, { useState } from 'react';
import {
  BookOpen,
  PieChart,
  PiggyBank,
  TrendingUp,
  ShieldCheck,
  CreditCard,
  Percent,
  Calculator,
  ChevronRight,
  Sparkles,
} from 'lucide-react';

const TOPICS = [
  {
    id: 'budgeting',
    title: 'Budgeting & 50/30/20 Rule',
    icon: PieChart,
    color: 'from-blue-500 to-indigo-600',
    shortDesc: 'Master cashflow planning with the popular 50/30/20 framework to balance living, enjoyment, and future wealth.',
    explanation:
      'Budgeting is the foundational practice of tracking where every rupee comes from and where it goes. Rather than restricting your life, a good budget grants you permission to spend mindfully while guaranteeing you save for future goals.',
    keyPoints: [
      '50% Needs: Essential expenditures like housing, groceries, utilities, and basic transportation.',
      '30% Wants: Non-essential lifestyle expenses like dining out, entertainment, and hobbies.',
      '20% Savings & Debt: Building emergency funds, investments (SIP), and extra debt payments.',
      'Zero-Based Budgeting: Give every rupee a job before the month starts so nothing leaks.',
    ],
    example:
      'If your monthly in-hand income is ₹50,000, allocate ₹25,000 to rent and groceries, ₹15,000 to dining and entertainment, and ₹10,000 directly into savings and investments.',
  },
  {
    id: 'saving',
    title: 'Smart Saving Habits',
    icon: PiggyBank,
    color: 'from-emerald-500 to-teal-600',
    shortDesc: 'Automate your savings to pay yourself first before discretionary expenses can erode your surplus.',
    explanation:
      'Saving money is not about what is left over at the end of the month—it is about consciously "paying yourself first" the day your salary lands. Establishing this discipline prevents lifestyle inflation.',
    keyPoints: [
      'Pay Yourself First: Transfer a predetermined percentage of your income to savings immediately on payday.',
      'Separate Accounts: Keep an everyday spending account separate from your high-yield savings or investment account.',
      '30-Day Rule for Discretionary Purchases: Wait 30 days before making large impulse buys to assess genuine desire.',
      'Track Micro-Expenses: Small recurring subscriptions often aggregate into substantial sums annually.',
    ],
    example:
      'Setting up an auto-debit of ₹5,000 on the 1st of every month ensures ₹60,000 in saved principal each year before incidental spending occurs.',
  },
  {
    id: 'compound-interest',
    title: 'Compound Interest: The 8th Wonder',
    icon: Percent,
    color: 'from-purple-500 to-violet-600',
    shortDesc: 'Understand how earning returns on your previous returns turns consistent investing into exponential growth over time.',
    explanation:
      'Compound interest occurs when interest or investment yield is added back to the principal, so that from that moment on, the added interest itself also earns interest. Over long periods (10-25 years), compounding can dwarf your actual contributions.',
    keyPoints: [
      'Formula: A = P(1 + r/n)^(nt), where compounding frequency and time exponentiate capital.',
      'Time is the Greatest Multiplier: Starting 5 years earlier often yields twice the wealth of starting late with double the capital.',
      'Rule of 72: Divide 72 by your expected annual rate of return to approximate how many years it takes to double your money (e.g. 72 / 12% = 6 years).',
    ],
    example:
      'Investing ₹5,000/month at 12% annual return for 20 years results in a total investment of ₹12 Lakhs growing into approximately ₹50 Lakhs.',
  },
  {
    id: 'emergency-fund',
    title: 'Emergency Fund Essentials',
    icon: ShieldCheck,
    color: 'from-amber-500 to-orange-600',
    shortDesc: 'Create a financial safety buffer to insulate yourself from unexpected shocks, job transitions, or medical needs.',
    explanation:
      'An emergency fund is readily accessible money reserved exclusively for genuine unforeseen financial shocks. It acts as insurance that prevents you from going into high-interest debt or breaking long-term investments when life happens.',
    keyPoints: [
      'Target Size: Aim for 3 to 6 months of mandatory living expenses (rent, food, insurance, debt payments).',
      'High Liquidity: Keep this money in liquid instruments like high-yield savings accounts or liquid debt mutual funds.',
      'Do Not Chase Returns: The goal of an emergency reserve is safety and capital preservation, not aggressive appreciation.',
      'Replenish Immediately: If tapped, pausing other investments to restore the fund is top priority.',
    ],
    example:
      'If your baseline monthly survival needs cost ₹20,000, build a designated emergency buffer of ₹60,000 to ₹1,20,000 before initiating aggressive equity investments.',
  },
  {
    id: 'sip',
    title: 'Systematic Investment Plan (SIP)',
    icon: TrendingUp,
    color: 'from-indigo-500 to-cyan-600',
    shortDesc: 'Harness Rupee Cost Averaging and psychological discipline by investing fixed amounts automatically each month.',
    explanation:
      'A Systematic Investment Plan (SIP) is a disciplined method of investing a fixed sum regularly into mutual funds. It eliminates the futile anxiety of "timing the market" by purchasing more units when prices are low and fewer when prices are elevated.',
    keyPoints: [
      'Rupee Cost Averaging: Automatically lowers your average purchase cost over market cycles without guessing bottoms.',
      'Affordability: You can initiate SIPs starting as low as ₹500/month in broad index or diversified equity funds.',
      'Automated Habit: Money is deducted via bank mandate, building financial discipline naturally.',
      'Long-Term Horizon: Equities are volatile short term; SIPs shine best over 5+ year spans.',
    ],
    example:
      'If the market drops 10%, your regular ₹2,000 SIP simply buys 11% more fund units that month, setting up amplified gains when the market recovers.',
  },
  {
    id: 'mutual-funds',
    title: 'Mutual Funds Demystified',
    icon: BookOpen,
    color: 'from-teal-500 to-emerald-600',
    shortDesc: 'Learn how pooled investment vehicles provide instant diversification, professional management, and cost efficiency.',
    explanation:
      'A mutual fund collects capital from thousands of retail investors to purchase a diversified portfolio of stocks, bonds, or government securities managed by professional portfolio managers.',
    keyPoints: [
      'Diversification: Owning a single mutual fund unit can give you exposure to 50 to 500 individual companies.',
      'Types: Equity funds (high growth / volatility), Debt funds (stable income), Hybrid funds (balanced).',
      'Index Funds (Passive): Low-cost funds replicating benchmark indices (e.g. Nifty 50, S&P 500) with ultra-low expense ratios.',
      'Expense Ratio: The annual percentage fee deducted for fund operations—always look for lower expense ratios.',
    ],
    example:
      'Instead of having to research and buy shares in 50 top companies individually, one index mutual fund lets you own a slice of all 50 seamlessly.',
  },
  {
    id: 'credit-score',
    title: 'Credit Score & Responsible Debt',
    icon: CreditCard,
    color: 'from-rose-500 to-pink-600',
    shortDesc: 'Understand CIBIL/Credit scores, credit utilization ratios, and how to borrow smartly without debt traps.',
    explanation:
      'A credit score (typically between 300 and 900) represents your creditworthiness to lenders. A high score unlocks lower interest rates on mortgages, car loans, and business financing.',
    keyPoints: [
      'Payment History (35% weight): Always pay 100% of your credit card statement on or before the due date.',
      'Credit Utilization (30% weight): Keep credit card spending below 30% of your approved credit limit.',
      'Credit Age: Maintain older credit lines active to establish a demonstrable track record.',
      'Target Score: A score of 750 or higher qualifies you for the best lending tiers and lowest interest rates.',
    ],
    example:
      'If your credit card limit is ₹1,00,000, aim not to carry a statement balance higher than ₹30,000 during your billing cycle.',
  },
];

const LearningCenter = () => {
  const [selectedTopic, setSelectedTopic] = useState(TOPICS[0]);

  // Interactive Compound Interest / SIP Calculator State
  const [calcMonthly, setCalcMonthly] = useState(5000);
  const [calcRate, setCalcRate] = useState(12);
  const [calcYears, setCalcYears] = useState(15);

  // SIP Future Value formula: FV = P * [((1 + i)^n - 1) / i] * (1 + i)
  const calculateSIP = () => {
    const P = parseFloat(calcMonthly) || 0;
    const i = (parseFloat(calcRate) || 0) / 100 / 12;
    const n = (parseFloat(calcYears) || 0) * 12;
    if (i === 0 || n === 0) return { totalInvested: P * n, futureValue: P * n, returns: 0 };

    const futureValue = P * ((Math.pow(1 + i, n) - 1) / i) * (1 + i);
    const totalInvested = P * n;
    const returns = futureValue - totalInvested;

    return {
      totalInvested: Math.round(totalInvested),
      futureValue: Math.round(futureValue),
      returns: Math.round(returns),
    };
  };

  const { totalInvested, futureValue, returns } = calculateSIP();

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <BookOpen className="w-7 h-7 text-indigo-600" />
          Financial Education Center
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Essential personal finance principles, terminology, and interactive calculators for students and beginners
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Topic Selector List */}
        <div className="lg:col-span-4 space-y-2">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider px-2 mb-3">
            Core Modules
          </h2>
          {TOPICS.map((topic) => {
            const Icon = topic.icon;
            const isSelected = selectedTopic.id === topic.id;
            return (
              <button
                key={topic.id}
                onClick={() => setSelectedTopic(topic)}
                className={`w-full text-left p-3.5 rounded-xl border transition-all flex items-center justify-between cursor-pointer ${
                  isSelected
                    ? 'bg-white border-indigo-500 shadow-sm ring-2 ring-indigo-100'
                    : 'bg-white/60 border-slate-200 hover:bg-white hover:border-slate-300'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-8 h-8 rounded-lg bg-gradient-to-tr ${topic.color} text-white flex items-center justify-center shrink-0 shadow-xs`}
                  >
                    <Icon className="w-4 h-4" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-slate-900">{topic.title}</h3>
                    <p className="text-xs text-slate-500 line-clamp-1 mt-0.5">{topic.shortDesc}</p>
                  </div>
                </div>
                <ChevronRight
                  className={`w-4 h-4 shrink-0 transition-transform ${
                    isSelected ? 'text-indigo-600 translate-x-0.5' : 'text-slate-300'
                  }`}
                />
              </button>
            );
          })}
        </div>

        {/* Selected Topic Detail Card */}
        <div className="lg:col-span-8 space-y-6">
          <div className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-xs">
            {/* Topic Header */}
            <div className="flex items-center gap-4 pb-6 border-b border-slate-100">
              <div
                className={`w-12 h-12 rounded-2xl bg-gradient-to-tr ${selectedTopic.color} text-white flex items-center justify-center shadow-md`}
              >
                <selectedTopic.icon className="w-6 h-6" />
              </div>
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">
                  Topic Guide
                </span>
                <h2 className="text-xl font-bold text-slate-900">{selectedTopic.title}</h2>
              </div>
            </div>

            {/* Explanation */}
            <div className="mt-6 space-y-4">
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1.5">
                  Overview
                </h4>
                <p className="text-sm text-slate-700 leading-relaxed">{selectedTopic.explanation}</p>
              </div>

              {/* Key Points */}
              <div className="pt-2">
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                  Key Rules & Takeaways
                </h4>
                <div className="space-y-2.5">
                  {selectedTopic.keyPoints.map((point, idx) => (
                    <div
                      key={idx}
                      className="flex items-start gap-2.5 text-sm text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100"
                    >
                      <span className="w-5 h-5 rounded-full bg-indigo-100 text-indigo-700 text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                        {idx + 1}
                      </span>
                      <span className="leading-snug">{point}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Practical Example */}
              <div className="pt-2">
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1.5">
                  Practical Example
                </h4>
                <div className="p-4 bg-indigo-50/70 border border-indigo-100 rounded-xl text-sm text-indigo-950 flex items-start gap-3">
                  <Sparkles className="w-5 h-5 text-indigo-600 shrink-0 mt-0.5" />
                  <p className="leading-relaxed">{selectedTopic.example}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Interactive SIP / Compounding Calculator Widget */}
          <div className="bg-gradient-to-br from-slate-900 to-indigo-950 text-white border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-md">
            <div className="flex items-center gap-3 pb-4 border-b border-white/10">
              <Calculator className="w-6 h-6 text-indigo-400" />
              <div>
                <h3 className="text-base font-bold">Interactive SIP & Compounding Calculator</h3>
                <p className="text-xs text-indigo-200">
                  Experiment with monthly investments and see the power of compounding in action
                </p>
              </div>
            </div>

            <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs text-indigo-200 mb-1 font-medium">
                  Monthly Investment (₹)
                </label>
                <input
                  type="number"
                  step="500"
                  min="500"
                  value={calcMonthly}
                  onChange={(e) => setCalcMonthly(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-xl text-white font-semibold text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                />
              </div>
              <div>
                <label className="block text-xs text-indigo-200 mb-1 font-medium">
                  Expected Return (% p.a.)
                </label>
                <input
                  type="number"
                  step="0.5"
                  min="1"
                  max="30"
                  value={calcRate}
                  onChange={(e) => setCalcRate(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-xl text-white font-semibold text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                />
              </div>
              <div>
                <label className="block text-xs text-indigo-200 mb-1 font-medium">
                  Time Period (Years)
                </label>
                <input
                  type="number"
                  min="1"
                  max="40"
                  value={calcYears}
                  onChange={(e) => setCalcYears(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-white/10 border border-white/20 rounded-xl text-white font-semibold text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                />
              </div>
            </div>

            {/* Results Display */}
            <div className="mt-6 pt-6 border-t border-white/10 grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
              <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                <span className="text-[11px] text-indigo-200 uppercase tracking-wider block">
                  Total Invested
                </span>
                <span className="text-lg font-bold text-white mt-1 block">
                  ₹{totalInvested.toLocaleString('en-IN')}
                </span>
              </div>
              <div className="p-3 bg-white/5 rounded-xl border border-white/10">
                <span className="text-[11px] text-emerald-300 uppercase tracking-wider block">
                  Est. Wealth Gain
                </span>
                <span className="text-lg font-bold text-emerald-400 mt-1 block">
                  ₹{returns.toLocaleString('en-IN')}
                </span>
              </div>
              <div className="p-3 bg-indigo-500/20 rounded-xl border border-indigo-400/30">
                <span className="text-[11px] text-indigo-300 uppercase tracking-wider block">
                  Expected Corpus
                </span>
                <span className="text-xl font-extrabold text-white mt-1 block">
                  ₹{futureValue.toLocaleString('en-IN')}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LearningCenter;
