import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/client';
import {
  TrendingUp,
  TrendingDown,
  PiggyBank,
  Wallet,
  Receipt,
  Bot,
  ArrowUpRight,
  ArrowDownRight,
  Loader2,
  AlertCircle,
  PieChart as PieChartIcon,
  BarChart3,
  Percent,
} from 'lucide-react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from 'recharts';

const PIE_COLORS = [
  '#f43f5e', // rose
  '#3b82f6', // blue
  '#8b5cf6', // purple
  '#f59e0b', // amber
  '#ec4899', // pink
  '#10b981', // emerald
  '#f97316', // orange
  '#64748b', // slate
];

const Dashboard = () => {
  const [summary, setSummary] = useState({
    total_income: 0,
    total_expenses: 0,
    savings: 0,
  });
  const [categoryData, setCategoryData] = useState([]);
  const [monthlyTrend, setMonthlyTrend] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [sumRes, catRes, trendRes] = await Promise.all([
        api.get('/dashboard/summary'),
        api.get('/dashboard/category-breakdown'),
        api.get('/dashboard/monthly-trend'),
      ]);

      setSummary(sumRes.data);
      setCategoryData(catRes.data);
      setMonthlyTrend(trendRes.data);
      setError('');
    } catch (err) {
      setError('Failed to load dashboard data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const savingsRate =
    summary.total_income > 0
      ? Math.max(0, Math.round((summary.savings / summary.total_income) * 100))
      : 0;

  if (loading) {
    return (
      <div className="py-24 text-center flex flex-col items-center justify-center">
        <Loader2 className="w-10 h-10 text-indigo-600 animate-spin" />
        <p className="mt-4 text-sm font-medium text-slate-600">Loading your financial dashboard...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Top Header & Quick Actions */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Financial Overview</h1>
          <p className="text-sm text-slate-500 mt-1">
            Real-time snapshot of your income, expenses, and personal savings progress
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/income"
            className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 rounded-xl transition-colors shadow-2xs"
          >
            <Wallet className="w-4 h-4" />
            <span>+ Add Income</span>
          </Link>
          <Link
            to="/expenses"
            className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200 rounded-xl transition-colors shadow-2xs"
          >
            <Receipt className="w-4 h-4" />
            <span>+ Add Expense</span>
          </Link>
          <Link
            to="/mentor"
            className="inline-flex items-center gap-1.5 px-4 py-2 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl transition-colors shadow-2xs"
          >
            <Bot className="w-4 h-4" />
            <span>Ask AI Mentor</span>
          </Link>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-800 rounded-xl flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 shrink-0" />
          <span className="text-sm font-medium">{error}</span>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        {/* Total Income Card */}
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Total Income</span>
            <div className="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <TrendingUp className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <div className="text-2xl font-black text-slate-900">
              ₹{summary.total_income.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
            </div>
            <div className="mt-1 flex items-center text-xs text-emerald-600 font-semibold">
              <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" />
              <span>Inflow streams</span>
            </div>
          </div>
        </div>

        {/* Total Expenses Card */}
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Total Expenses</span>
            <div className="w-9 h-9 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center">
              <TrendingDown className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <div className="text-2xl font-black text-slate-900">
              ₹{summary.total_expenses.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
            </div>
            <div className="mt-1 flex items-center text-xs text-rose-600 font-semibold">
              <ArrowDownRight className="w-3.5 h-3.5 mr-0.5" />
              <span>Outgoings logged</span>
            </div>
          </div>
        </div>

        {/* Net Savings Card */}
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Net Savings</span>
            <div
              className={`w-9 h-9 rounded-xl flex items-center justify-center ${
                summary.savings >= 0 ? 'bg-indigo-50 text-indigo-600' : 'bg-amber-50 text-amber-600'
              }`}
            >
              <PiggyBank className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <div
              className={`text-2xl font-black ${
                summary.savings >= 0 ? 'text-indigo-600' : 'text-amber-600'
              }`}
            >
              ₹{summary.savings.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
            </div>
            <div className="mt-1 flex items-center text-xs text-slate-500">
              <span>{summary.savings >= 0 ? 'Income surplus' : 'Deficit / overspending'}</span>
            </div>
          </div>
        </div>

        {/* Savings Rate Card */}
        <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Savings Rate</span>
            <div className="w-9 h-9 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center">
              <Percent className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <div className="text-2xl font-black text-slate-900">{savingsRate}%</div>
            <div className="mt-1 flex items-center text-xs text-slate-500">
              <span>Benchmark target: 20%+</span>
            </div>
          </div>
        </div>
      </div>

      {/* Visualizations Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Category Breakdown Donut / Pie Chart */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <PieChartIcon className="w-4 h-4 text-indigo-600" />
                Expense Breakdown by Category
              </h2>
              <p className="text-xs text-slate-500">Where your money goes</p>
            </div>
          </div>

          {categoryData.length === 0 ? (
            <div className="h-64 flex flex-col items-center justify-center text-slate-400 text-center p-4">
              <Receipt className="w-10 h-10 mb-2 stroke-1" />
              <p className="text-sm font-medium">No expense categories to show</p>
              <p className="text-xs text-slate-400 mt-1">Add expenses to visualize your spending distribution.</p>
            </div>
          ) : (
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={categoryData}
                    dataKey="amount"
                    nameKey="category"
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={85}
                    paddingAngle={4}
                  >
                    {categoryData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={PIE_COLORS[index % PIE_COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(value) => [
                      `₹${Number(value).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`,
                      'Spent',
                    ]}
                  />
                  <Legend
                    verticalAlign="bottom"
                    height={36}
                    formatter={(value, entry) => (
                      <span className="text-xs text-slate-700 font-medium">{value}</span>
                    )}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>

        {/* Monthly Trend Chart */}
        <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-indigo-600" />
                Monthly Cashflow Trend
              </h2>
              <p className="text-xs text-slate-500">Income vs Expenses vs Savings</p>
            </div>
          </div>

          {monthlyTrend.length === 0 ? (
            <div className="h-64 flex flex-col items-center justify-center text-slate-400 text-center p-4">
              <BarChart3 className="w-10 h-10 mb-2 stroke-1" />
              <p className="text-sm font-medium">No monthly trend data available</p>
              <p className="text-xs text-slate-400 mt-1">
                Log income and expenses across dates to generate monthly cashflow trends.
              </p>
            </div>
          ) : (
            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={monthlyTrend} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="month" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip
                    formatter={(val) => [
                      `₹${Number(val).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`,
                    ]}
                  />
                  <Legend
                    wrapperStyle={{ fontSize: '12px' }}
                    verticalAlign="bottom"
                    height={36}
                  />
                  <Bar dataKey="income" name="Income" fill="#10b981" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="expenses" name="Expenses" fill="#f43f5e" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="savings" name="Savings" fill="#6366f1" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      </div>

      {/* AI Educational Teaser Banner */}
      <div className="bg-gradient-to-r from-indigo-900 to-violet-900 rounded-2xl p-6 text-white shadow-sm flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-2 text-center md:text-left">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 text-xs font-semibold text-indigo-200">
            <Bot className="w-3.5 h-3.5" />
            AI Financial Mentor Ready
          </div>
          <h3 className="text-lg font-bold">Need assistance with your financial planning?</h3>
          <p className="text-sm text-indigo-200 max-w-xl">
            Ask our AI mentor about compound interest, SIP strategies, emergency fund targets, or request an evaluation of your current spending habits.
          </p>
        </div>
        <Link
          to="/mentor"
          className="shrink-0 px-5 py-2.5 bg-white text-indigo-900 hover:bg-indigo-50 font-bold text-sm rounded-xl transition-colors shadow-sm"
        >
          Consult AI Mentor &rarr;
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;
