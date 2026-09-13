import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/client';
import {
  Compass,
  Wallet,
  Receipt,
  PiggyBank,
  Percent,
  Coins,
  Shield,
  Clock,
  Target,
  Bot,
  ArrowRight,
  AlertTriangle,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Loader2,
  Sparkles,
  Edit3,
} from 'lucide-react';

const priorityBadges = {
  HIGH: 'bg-rose-100 text-rose-800 border-rose-200',
  MEDIUM: 'bg-indigo-100 text-indigo-800 border-indigo-200',
  LOW: 'bg-slate-100 text-slate-700 border-slate-200',
};

const readinessBadges = {
  NOT_READY: {
    label: 'Stabilize Cashflow',
    color: 'bg-red-50 text-red-700 border-red-200',
    icon: AlertCircle,
  },
  BUILD_EMERGENCY_FUND: {
    label: 'Build Emergency Buffer',
    color: 'bg-amber-50 text-amber-700 border-amber-200',
    icon: Shield,
  },
  READY_TO_EXPLORE: {
    label: 'Ready to Explore SIPs',
    color: 'bg-indigo-50 text-indigo-700 border-indigo-200',
    icon: CheckCircle2,
  },
  STRONG_INVESTMENT_CAPACITY: {
    label: 'Strong Investment Capacity',
    color: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    icon: Sparkles,
  },
};

const Recommendations = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      const res = await api.get('/recommendations');
      setData(res.data);
      setError('');
    } catch (err) {
      setError('Unable to load recommendations. Please ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const handleAskMentor = (question) => {
    navigate('/mentor', { state: { prefilledQuery: question } });
  };

  if (loading) {
    return (
      <div className="py-24 text-center flex flex-col items-center justify-center">
        <Loader2 className="w-10 h-10 text-indigo-600 animate-spin" />
        <p className="mt-4 text-sm font-medium text-slate-600">
          Synthesizing your personalized financial recommendations...
        </p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="p-6 bg-red-50 border border-red-200 rounded-2xl text-center space-y-3">
        <AlertCircle className="w-8 h-8 text-red-600 mx-auto" />
        <p className="text-sm font-semibold text-red-800">{error || 'Something went wrong.'}</p>
        <button
          onClick={fetchRecommendations}
          className="px-4 py-2 bg-red-600 text-white rounded-xl text-xs font-semibold hover:bg-red-700"
        >
          Try Again
        </button>
      </div>
    );
  }

  const { financial_summary, profile, recommendations } = data;
  const readinessMeta = readinessBadges[financial_summary.investment_readiness] || readinessBadges.READY_TO_EXPLORE;
  const ReadinessIcon = readinessMeta.icon;

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Compass className="w-7 h-7 text-indigo-600" />
            Personalized Educational Recommendations
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Rule-based financial diagnostics grounded in your actual income, expenses, and stated goals
          </p>
        </div>
        <Link
          to="/profile"
          className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 rounded-xl transition-colors shadow-2xs self-start"
        >
          <Edit3 className="w-3.5 h-3.5" />
          <span>{profile ? 'Edit Investor Profile' : 'Configure Profile'}</span>
        </Link>
      </div>

      {/* Missing Profile Reminder Banner */}
      {!profile && (
        <div className="p-4 bg-amber-50 border border-amber-200 rounded-2xl flex items-start justify-between gap-4">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
            <div>
              <h4 className="text-sm font-bold text-amber-900">Your Investor Profile is Incomplete</h4>
              <p className="text-xs text-amber-800 mt-0.5">
                We are currently assuming default settings. Complete your profile to customize guidance to your exact age, risk comfort, and timeline.
              </p>
            </div>
          </div>
          <Link
            to="/profile"
            className="px-3.5 py-1.5 bg-amber-600 text-white rounded-lg text-xs font-semibold hover:bg-amber-700 shrink-0"
          >
            Complete Profile
          </Link>
        </div>
      )}

      {/* Financial Snapshot KPI Bar */}
      <div>
        <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
          Your Calculated Financial Snapshot
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          {/* Monthly Income */}
          <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              Monthly Inflow
            </span>
            <div className="text-xl font-extrabold text-slate-900 mt-1">
              ₹{financial_summary.monthly_income.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
            </div>
            <div className="text-[10px] text-emerald-600 font-semibold mt-0.5 flex items-center gap-0.5">
              <Wallet className="w-3 h-3" /> Average income
            </div>
          </div>

          {/* Monthly Expenses */}
          <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              Monthly Outflow
            </span>
            <div className="text-xl font-extrabold text-slate-900 mt-1">
              ₹{financial_summary.monthly_expenses.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
            </div>
            <div className="text-[10px] text-rose-600 font-semibold mt-0.5 flex items-center gap-0.5">
              <Receipt className="w-3 h-3" /> Recorded expenses
            </div>
          </div>

          {/* Monthly Surplus */}
          <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              Monthly Surplus
            </span>
            <div
              className={`text-xl font-extrabold mt-1 ${
                financial_summary.monthly_savings >= 0 ? 'text-indigo-600' : 'text-amber-600'
              }`}
            >
              {financial_summary.monthly_savings < 0
                ? `-₹${Math.abs(financial_summary.monthly_savings).toLocaleString('en-IN', { maximumFractionDigits: 0 })}`
                : `₹${financial_summary.monthly_savings.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`}
            </div>
            <div className="text-[10px] text-slate-500 font-semibold mt-0.5 flex items-center gap-0.5">
              <PiggyBank className="w-3 h-3" /> Income - Expenses
            </div>
          </div>

          {/* Savings Rate */}
          <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-xs">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              Savings Rate
            </span>
            <div className="text-xl font-extrabold text-slate-900 mt-1">
              {financial_summary.savings_rate}%
            </div>
            <div className="text-[10px] text-slate-500 font-semibold mt-0.5 flex items-center gap-0.5">
              <Percent className="w-3 h-3" /> Target: 20%+
            </div>
          </div>

          {/* Estimated Investment Capacity */}
          <div className="bg-gradient-to-br from-indigo-50 to-violet-50 border border-indigo-100 rounded-2xl p-4 shadow-xs col-span-2 sm:col-span-1">
            <span className="text-[11px] font-bold text-indigo-700 uppercase tracking-wider block">
              Est. Monthly Capacity
            </span>
            <div className="text-xl font-black text-indigo-900 mt-1">
              ₹{financial_summary.investment_capacity.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
            </div>
            <div className="text-[10px] text-indigo-600 font-semibold mt-0.5 flex items-center gap-0.5">
              <Coins className="w-3 h-3" /> Conservative buffer
            </div>
          </div>
        </div>
      </div>

      {/* Investor Profile & Readiness Card */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center gap-3">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
              Investment Readiness:
            </span>
            <span
              className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold border ${readinessMeta.color}`}
            >
              <ReadinessIcon className="w-3.5 h-3.5" />
              {readinessMeta.label}
            </span>
          </div>
          <p className="text-sm text-slate-700 max-w-2xl leading-relaxed">
            {financial_summary.investment_readiness_explanation}
          </p>
        </div>

        {/* Profile Pill Badges */}
        <div className="flex flex-wrap gap-2 text-xs shrink-0">
          <div className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl flex items-center gap-1.5 text-slate-700">
            <Shield className="w-3.5 h-3.5 text-indigo-600" />
            <span>Risk: <strong>{profile?.risk_tolerance || 'Moderate'}</strong></span>
          </div>
          <div className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl flex items-center gap-1.5 text-slate-700">
            <Clock className="w-3.5 h-3.5 text-indigo-600" />
            <span>Horizon: <strong>{profile?.investment_horizon || '5–10 yrs'}</strong></span>
          </div>
          <div className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl flex items-center gap-1.5 text-slate-700">
            <Target className="w-3.5 h-3.5 text-indigo-600" />
            <span>Goal: <strong>{profile?.financial_goal || 'Wealth'}</strong></span>
          </div>
          <div className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-xl flex items-center gap-1.5 text-slate-700">
            <PiggyBank className="w-3.5 h-3.5 text-emerald-600" />
            <span>Emergency: <strong>~{financial_summary.estimated_emergency_months} mo</strong></span>
          </div>
        </div>
      </div>

      {/* Prioritized Recommendations Section */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Your Mentor's Actionable Recommendations ({recommendations.length})
          </h2>
          <span className="text-xs text-slate-400 italic">Sorted by rule priority</span>
        </div>

        {recommendations.length === 0 ? (
          <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center text-slate-500">
            <Compass className="w-10 h-10 mx-auto text-slate-400 mb-2" />
            <p className="text-sm font-semibold">No active recommendations right now.</p>
            <p className="text-xs mt-1">Log your income and expenses to generate custom financial pathways.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {recommendations.map((rec) => (
              <div
                key={rec.id}
                className="bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-xs hover:shadow-sm transition-shadow space-y-4"
              >
                {/* Title & Priority Header */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-center gap-3">
                    <span
                      className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider border ${
                        priorityBadges[rec.priority] || priorityBadges.LOW
                      }`}
                    >
                      {rec.priority} Priority
                    </span>
                    <h3 className="text-base font-bold text-slate-900">{rec.title}</h3>
                  </div>
                  <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                    Category: {rec.category.replace(/_/g, ' ')}
                  </span>
                </div>

                {/* Reason & Explanation */}
                <div className="space-y-2 text-sm text-slate-700">
                  <p>
                    <strong className="text-slate-900">Why this matters for you:</strong> {rec.reason}
                  </p>
                  <p className="text-slate-600 leading-relaxed">{rec.explanation}</p>
                </div>

                {/* Suggested Action Bar */}
                <div className="p-3.5 bg-indigo-50/70 border border-indigo-100 rounded-xl flex items-start sm:items-center justify-between gap-4">
                  <div className="flex items-start gap-2.5">
                    <Sparkles className="w-4 h-4 text-indigo-600 shrink-0 mt-0.5" />
                    <div className="text-xs text-indigo-950 font-medium leading-snug">
                      <strong className="text-indigo-900 font-bold">Recommended Step:</strong>{' '}
                      {rec.suggested_action}
                    </div>
                  </div>
                  <button
                    onClick={() => handleAskMentor(`Can you explain more about this recommendation: "${rec.title}"?`)}
                    className="shrink-0 text-xs font-bold text-indigo-700 hover:text-indigo-900 flex items-center gap-1 cursor-pointer"
                  >
                    <span>Ask Mentor</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Ask Your Mentor Quick Chips */}
      <div className="bg-gradient-to-r from-indigo-900 to-violet-900 rounded-2xl p-6 sm:p-8 text-white shadow-md space-y-4">
        <div className="flex items-center gap-3">
          <Bot className="w-6 h-6 text-indigo-300" />
          <div>
            <h3 className="text-lg font-bold">Have questions about these recommendations?</h3>
            <p className="text-xs text-indigo-200">
              Click any quick topic below to explore details directly with your AI Mentor:
            </p>
          </div>
        </div>

        <div className="flex flex-wrap gap-2.5 pt-2">
          {[
            'Can I afford to start investing?',
            'How much of my surplus should I invest every month?',
            'Why did you recommend mutual funds / SIP for me?',
            'Should I focus on building my emergency fund first?',
            'Am I saving enough money each month?',
          ].map((prompt, i) => (
            <button
              key={i}
              onClick={() => handleAskMentor(prompt)}
              className="px-3.5 py-2 bg-white/10 hover:bg-white/20 text-white border border-white/20 rounded-xl text-xs font-semibold transition-colors flex items-center gap-1.5 cursor-pointer"
            >
              <span>{prompt}</span>
              <ArrowRight className="w-3 h-3 text-indigo-300" />
            </button>
          ))}
        </div>
      </div>

      {/* Educational Disclaimer */}
      <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl text-[11px] text-slate-500 flex items-start gap-2.5 leading-relaxed">
        <HelpCircle className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
        <p>
          <strong>Educational Guidance Disclaimer:</strong> All evaluations, readiness classifications,
          and recommendations generated here are calculated using deterministic rule-based heuristics and educational models.
          They do not constitute certified financial, tax, or investment advice. Always perform independent diligence or
          consult a SEBI-registered advisor before executing financial contracts.
        </p>
      </div>
    </div>
  );
};

export default Recommendations;
