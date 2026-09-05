import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/client';
import {
  History,
  Bot,
  User,
  Trash2,
  Calendar,
  MessageSquare,
  Loader2,
  AlertCircle,
  CheckCircle,
} from 'lucide-react';

const ChatHistory = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const res = await api.get('/ai/history');
      setHistory(res.data);
      setError('');
    } catch (err) {
      setError('Unable to load chat history. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this conversation from your history?')) return;
    try {
      await api.delete(`/ai/history/${id}`);
      setHistory((prev) => prev.filter((item) => item.id !== id));
      setSuccess('Conversation record deleted.');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to delete history record.');
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <History className="w-7 h-7 text-indigo-600" />
            AI Chat History
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Review past questions asked to your AI Financial Mentor and recommendations given
          </p>
        </div>
        <Link
          to="/mentor"
          className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl transition-colors shadow-2xs self-start"
        >
          <Bot className="w-4 h-4" />
          <span>New AI Consultation</span>
        </Link>
      </div>

      {/* Alerts */}
      {success && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl flex items-center gap-3">
          <CheckCircle className="w-5 h-5 text-emerald-600 shrink-0" />
          <span className="text-sm font-medium">{success}</span>
        </div>
      )}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-800 rounded-xl flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-600 shrink-0" />
          <span className="text-sm font-medium">{error}</span>
        </div>
      )}

      {/* History Items */}
      {loading ? (
        <div className="py-24 text-center flex flex-col items-center justify-center">
          <Loader2 className="w-10 h-10 text-indigo-600 animate-spin" />
          <p className="mt-3 text-sm font-medium text-slate-600">Retrieving past discussions...</p>
        </div>
      ) : history.length === 0 ? (
        <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center">
          <div className="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3">
            <MessageSquare className="w-6 h-6" />
          </div>
          <h3 className="text-base font-semibold text-slate-900">No chat history found</h3>
          <p className="text-sm text-slate-500 mt-1 max-w-sm mx-auto">
            You have not had any recorded interactions with the AI Mentor yet.
          </p>
          <Link
            to="/mentor"
            className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-xl text-xs font-semibold hover:bg-indigo-700 transition-colors"
          >
            <Bot className="w-4 h-4" />
            <span>Ask Your First Question</span>
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {history.map((item) => (
            <div
              key={item.id}
              className="bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-xs transition-shadow hover:shadow-sm"
            >
              {/* Header with date and delete button */}
              <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-100 text-xs text-slate-400">
                <span className="flex items-center gap-1.5 font-medium">
                  <Calendar className="w-3.5 h-3.5" />
                  {item.created_at
                    ? new Date(item.created_at).toLocaleString()
                    : 'Recorded conversation'}
                </span>
                <button
                  onClick={() => handleDelete(item.id)}
                  className="text-slate-400 hover:text-red-600 p-1 rounded-md transition-colors cursor-pointer"
                  title="Delete conversation"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>

              {/* Question */}
              <div className="flex items-start gap-3 mb-4">
                <div className="w-7 h-7 rounded-lg bg-indigo-600 text-white flex items-center justify-center shrink-0 mt-0.5">
                  <User className="w-4 h-4" />
                </div>
                <div className="text-sm font-semibold text-slate-900 leading-relaxed">
                  {item.user_message}
                </div>
              </div>

              {/* AI Answer */}
              <div className="flex items-start gap-3 bg-slate-50 border border-slate-200/70 rounded-xl p-4">
                <div className="w-7 h-7 rounded-lg bg-indigo-100 text-indigo-700 flex items-center justify-center shrink-0 mt-0.5">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="text-sm text-slate-700 leading-relaxed whitespace-pre-wrap">
                  {item.ai_response}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ChatHistory;
