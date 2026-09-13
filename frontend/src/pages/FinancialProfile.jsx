import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/client';
import {
  UserCheck,
  Shield,
  Clock,
  Target,
  PiggyBank,
  TrendingDown,
  Sparkles,
  CheckCircle,
  AlertCircle,
  Loader2,
  ArrowRight,
} from 'lucide-react';

const RISK_OPTIONS = [
  {
    value: 'Conservative',
    label: 'Conservative',
    desc: 'Prioritize capital safety and low volatility over aggressive returns (Debt, FDs, PPF).',
  },
  {
    value: 'Moderate',
    label: 'Moderate',
    desc: 'Seek a balance of inflation-beating growth and stability (Index & Hybrid funds).',
  },
  {
    value: 'Aggressive',
    label: 'Aggressive',
    desc: 'Maximize long-term wealth growth, comfortable with short-term market dips (Equity & Flexi-cap).',
  },
];

const HORIZON_OPTIONS = [
  { value: 'Less than 3 years', label: 'Less than 3 years (Short Term)' },
  { value: '3–5 years', label: '3–5 years (Medium Term)' },
  { value: '5–10 years', label: '5–10 years (Long Term)' },
  { value: 'More than 10 years', label: 'More than 10 years (Very Long Term)' },
];

const GOAL_OPTIONS = [
  'Wealth creation',
  'Retirement',
  'Buying a house',
  'Education',
  'Short-term savings',
  'General investing',
];

const BEHAVIOR_OPTIONS = [
  'Sell immediately to prevent further loss',
  'Feel concerned but continue holding',
  'Continue regular monthly investing through the dip',
  'Invest more capital while valuations are discounted',
];

const FinancialProfile = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const [formData, setFormData] = useState({
    age: 22,
    risk_tolerance: 'Moderate',
    investment_horizon: '5–10 years',
    financial_goal: 'Wealth creation',
    emergency_fund: '',
    risk_behavior: 'Continue regular monthly investing through the dip',
  });

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        setLoading(true);
        const res = await api.get('/profile');
        if (res.data) {
          setFormData({
            age: res.data.age || 22,
            risk_tolerance: res.data.risk_tolerance || 'Moderate',
            investment_horizon: res.data.investment_horizon || '5–10 years',
            financial_goal: res.data.financial_goal || 'Wealth creation',
            emergency_fund: res.data.emergency_fund || 0,
            risk_behavior: res.data.risk_behavior || 'Continue regular monthly investing through the dip',
          });
        }
      } catch (err) {
        // Not configured yet is fine
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'age' || name === 'emergency_fund' ? (value === '' ? '' : Number(value)) : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setErrorMsg('');
    setSuccessMsg('');

    const payload = {
      age: formData.age ? Number(formData.age) : null,
      risk_tolerance: formData.risk_tolerance,
      investment_horizon: formData.investment_horizon,
      financial_goal: formData.financial_goal,
      emergency_fund: Number(formData.emergency_fund) || 0.0,
      risk_behavior: formData.risk_behavior,
    };

    try {
      await api.post('/profile', payload);
      setSuccessMsg('Your financial profile has been saved! Your mentor will now use this information to personalize its guidance.');
      setTimeout(() => {
        navigate('/recommendations');
      }, 1800);
    } catch (err) {
      setErrorMsg(err.response?.data?.detail || 'Failed to save profile. Please check your inputs.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="py-24 text-center flex flex-col items-center justify-center">
        <Loader2 className="w-10 h-10 text-indigo-600 animate-spin" />
        <p className="mt-4 text-sm font-medium text-slate-600">Loading your investor profile...</p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
          <UserCheck className="w-7 h-7 text-indigo-600" />
          Personalize Your Financial Profile
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Tell your AI Mentor about your goals, risk comfort, and timeline to receive tailored educational guidance.
        </p>
      </div>

      {/* Alerts */}
      {successMsg && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl flex items-center gap-3">
          <CheckCircle className="w-5 h-5 text-emerald-600 shrink-0" />
          <div className="text-sm">
            <p className="font-semibold">{successMsg}</p>
            <p className="text-emerald-700 text-xs mt-0.5">Redirecting to your recommendations...</p>
          </div>
        </div>
      )}
      {errorMsg && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-800 rounded-xl flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 shrink-0" />
          <span className="text-sm font-medium">{errorMsg}</span>
        </div>
      )}

      {/* Profile Form */}
      <form onSubmit={handleSubmit} className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-xs space-y-6">
        {/* Section: Basic & Emergency Fund */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1">
              Your Age
            </label>
            <input
              type="number"
              name="age"
              min="16"
              max="120"
              required
              value={formData.age}
              onChange={handleChange}
              className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm text-slate-900 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              placeholder="21"
            />
            <p className="text-xs text-slate-400 mt-1">Helps determine your compounding runway.</p>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1 flex items-center gap-1.5">
              <PiggyBank className="w-4 h-4 text-emerald-600" />
              Current Emergency Savings (₹)
            </label>
            <input
              type="number"
              step="500"
              min="0"
              name="emergency_fund"
              value={formData.emergency_fund}
              onChange={handleChange}
              className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm text-slate-900 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              placeholder="e.g. 50000"
            />
            <p className="text-xs text-slate-400 mt-1">Money kept in savings or liquid funds for emergencies.</p>
          </div>
        </div>

        {/* Section: Risk Tolerance */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-2 flex items-center gap-1.5">
            <Shield className="w-4 h-4 text-indigo-600" />
            Risk Tolerance
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {RISK_OPTIONS.map((opt) => (
              <label
                key={opt.value}
                className={`p-3.5 rounded-xl border cursor-pointer transition-all flex flex-col justify-between ${
                  formData.risk_tolerance === opt.value
                    ? 'border-indigo-600 bg-indigo-50/60 ring-2 ring-indigo-200'
                    : 'border-slate-200 bg-white hover:border-slate-300'
                }`}
              >
                <div className="flex items-center justify-between mb-1.5">
                  <span className="text-sm font-bold text-slate-900">{opt.label}</span>
                  <input
                    type="radio"
                    name="risk_tolerance"
                    value={opt.value}
                    checked={formData.risk_tolerance === opt.value}
                    onChange={handleChange}
                    className="text-indigo-600 focus:ring-indigo-500"
                  />
                </div>
                <p className="text-xs text-slate-500 leading-relaxed">{opt.desc}</p>
              </label>
            ))}
          </div>
        </div>

        {/* Section: Investment Horizon & Goal */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1 flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-indigo-600" />
              Investment Horizon
            </label>
            <select
              name="investment_horizon"
              value={formData.investment_horizon}
              onChange={handleChange}
              className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm text-slate-900 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            >
              {HORIZON_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1 flex items-center gap-1.5">
              <Target className="w-4 h-4 text-indigo-600" />
              Primary Financial Goal
            </label>
            <select
              name="financial_goal"
              value={formData.financial_goal}
              onChange={handleChange}
              className="w-full px-3.5 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm text-slate-900 focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:outline-none"
            >
              {GOAL_OPTIONS.map((g) => (
                <option key={g} value={g}>
                  {g}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Section: Risk Behavior Question */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-700 mb-1.5 flex items-center gap-1.5">
            <TrendingDown className="w-4 h-4 text-amber-600" />
            Behavioral Check: If your portfolio temporarily dropped by 20%, what would you do?
          </label>
          <div className="space-y-2 mt-2">
            {BEHAVIOR_OPTIONS.map((choice) => (
              <label
                key={choice}
                className={`p-3 rounded-xl border text-sm flex items-center gap-3 cursor-pointer transition-colors ${
                  formData.risk_behavior === choice
                    ? 'border-indigo-600 bg-indigo-50/60 font-semibold text-indigo-950'
                    : 'border-slate-200 bg-slate-50/50 hover:bg-slate-50 text-slate-700'
                }`}
              >
                <input
                  type="radio"
                  name="risk_behavior"
                  value={choice}
                  checked={formData.risk_behavior === choice}
                  onChange={handleChange}
                  className="text-indigo-600 focus:ring-indigo-500"
                />
                <span>{choice}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Submit Bar */}
        <div className="pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-slate-400">
            You can update your profile anytime as your goals and income evolve.
          </p>
          <button
            type="submit"
            disabled={submitting}
            className="w-full sm:w-auto px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-xl transition-colors shadow-xs disabled:opacity-50 flex items-center justify-center gap-2 cursor-pointer"
          >
            {submitting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Saving Profile...</span>
              </>
            ) : (
              <>
                <span>Save Profile & View Recommendations</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default FinancialProfile;
