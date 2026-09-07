import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/client';
import {
  Bot,
  Send,
  Sparkles,
  User,
  AlertTriangle,
  History,
  Loader2,
} from 'lucide-react';

const SUGGESTED_PROMPTS = [
  'What are mutual funds and how do they work?',
  'What is a Systematic Investment Plan (SIP)?',
  'How should I build an emergency fund?',
  'Explain compound interest and the rule of 72.',
  'Analyze my current spending and budget.',
];

const renderInlineFormatting = (text, isUser = false) => {
  const parts = text.split(/(\*\*.*?\*\*|\*.*?\*|`.*?`)/g);
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return (
        <strong
          key={i}
          className={`font-semibold ${isUser ? 'text-white' : 'text-slate-900'}`}
        >
          {part.slice(2, -2)}
        </strong>
      );
    }
    if (part.startsWith('*') && part.endsWith('*')) {
      return (
        <em
          key={i}
          className={`italic ${isUser ? 'text-indigo-100' : 'text-slate-600'}`}
        >
          {part.slice(1, -1)}
        </em>
      );
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return (
        <code
          key={i}
          className="px-1.5 py-0.5 rounded bg-slate-200 text-xs font-mono text-indigo-700"
        >
          {part.slice(1, -1)}
        </code>
      );
    }
    return part;
  });
};

const FormattedMessage = ({ content, isUser }) => {
  if (!content) return null;
  if (isUser) {
    return <div className="leading-relaxed whitespace-pre-wrap">{content}</div>;
  }

  const lines = content.split('\n');

  return (
    <div className="space-y-1.5 text-sm leading-relaxed text-slate-800">
      {lines.map((line, idx) => {
        const trimmed = line.trim();
        if (!trimmed) {
          return <div key={idx} className="h-1" />;
        }
        if (trimmed.startsWith('### ')) {
          return (
            <h3 key={idx} className="text-base font-bold text-slate-900 mt-2 mb-1">
              {trimmed.replace('### ', '')}
            </h3>
          );
        }
        if (trimmed.startsWith('#### ')) {
          return (
            <h4
              key={idx}
              className="text-xs font-bold uppercase tracking-wider text-indigo-700 mt-2 mb-0.5"
            >
              {trimmed.replace('#### ', '')}
            </h4>
          );
        }
        if (trimmed.startsWith('> ')) {
          return (
            <blockquote
              key={idx}
              className="pl-3 border-l-2 border-indigo-400 italic text-slate-600 my-1.5"
            >
              {trimmed.replace('> ', '')}
            </blockquote>
          );
        }
        if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
          const itemText = trimmed.substring(2);
          return (
            <div key={idx} className="flex items-start gap-2 pl-2">
              <span className="text-indigo-500 font-bold">•</span>
              <span>{renderInlineFormatting(itemText)}</span>
            </div>
          );
        }
        if (/^\d+\.\s/.test(trimmed)) {
          const match = trimmed.match(/^(\d+)\.\s(.*)/);
          return (
            <div key={idx} className="flex items-start gap-2 pl-2">
              <span className="text-indigo-600 font-bold">{match[1]}.</span>
              <span>{renderInlineFormatting(match[2])}</span>
            </div>
          );
        }
        return <p key={idx}>{renderInlineFormatting(trimmed)}</p>;
      })}
    </div>
  );
};

const AIMentor = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        '### 👋 Welcome to your AI Financial Mentor!\n\n' +
        'I am trained to guide you through key personal finance principles, including **Mutual Funds**, **SIPs**, **Compound Interest**, **Emergency Funds**, **Budgeting**, and **Debt Management**.\n\n' +
        'You can also ask me about your real recorded expenses (e.g. *"Analyze my spending"* or *"Is my food expense high?"*).\n\n' +
        '*Disclaimer: All guidance is educational and does not constitute formal financial advice.*',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (textToSend) => {
    const query = textToSend || inputMessage;
    if (!query.trim() || loading) return;

    const userMsg = {
      role: 'user',
      content: query.trim(),
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputMessage('');
    setLoading(true);

    try {
      const res = await api.post('/ai/chat', { message: query.trim() });
      const aiReply = {
        role: 'assistant',
        content: res.data.ai_response,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => [...prev, aiReply]);
    } catch (err) {
      const errorReply = {
        role: 'assistant',
        content:
          'I apologize, but I was unable to process your request at this moment. Please check your connection or try again shortly.',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        isError: true,
      };
      setMessages((prev) => [...prev, errorReply]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Bot className="w-7 h-7 text-indigo-600" />
            AI Financial Mentor
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Ask questions, explore financial concepts, and gain insights into your cash flow
          </p>
        </div>
        <Link
          to="/history"
          className="inline-flex items-center gap-2 px-3.5 py-2 text-xs font-semibold text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 rounded-xl transition-colors shadow-2xs self-start"
        >
          <History className="w-4 h-4" />
          <span>View Past Conversations</span>
        </Link>
      </div>

      {/* Educational Disclaimer Banner */}
      <div className="bg-amber-50 border border-amber-200 rounded-xl p-3.5 flex items-start gap-3 text-amber-900 text-xs">
        <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        <p>
          <strong>Educational Guidance Only:</strong> Responses are generated for educational and
          informational purposes. This tool does not provide certified financial planning,
          guaranteed investment returns, or legal advice.
        </p>
      </div>

      {/* Chat Container */}
      <div className="bg-white border border-slate-200 rounded-2xl shadow-xs overflow-hidden flex flex-col h-[580px]">
        {/* Messages List */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex items-start gap-3 ${
                msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'
              }`}
            >
              {/* Avatar */}
              <div
                className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 ${
                  msg.role === 'user'
                    ? 'bg-indigo-600 text-white'
                    : msg.isError
                    ? 'bg-red-100 text-red-600'
                    : 'bg-indigo-100 text-indigo-700'
                }`}
              >
                {msg.role === 'user' ? (
                  <User className="w-4 h-4" />
                ) : (
                  <Bot className="w-4 h-4" />
                )}
              </div>

              {/* Message Bubble */}
              <div
                className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm shadow-2xs ${
                  msg.role === 'user'
                    ? 'bg-indigo-600 text-white rounded-tr-none'
                    : msg.isError
                    ? 'bg-red-50 text-red-900 border border-red-200 rounded-tl-none'
                    : 'bg-slate-100/90 text-slate-800 border border-slate-200/80 rounded-tl-none'
                }`}
              >
                <FormattedMessage content={msg.content} isUser={msg.role === 'user'} />
                <div
                  className={`text-[10px] mt-2 ${
                    msg.role === 'user' ? 'text-indigo-200 text-right' : 'text-slate-400'
                  }`}
                >
                  {msg.time}
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-xl bg-indigo-100 text-indigo-700 flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4" />
              </div>
              <div className="bg-slate-100 border border-slate-200/80 rounded-2xl rounded-tl-none px-4 py-3 flex items-center gap-2 text-sm text-slate-600">
                <Loader2 className="w-4 h-4 animate-spin text-indigo-600" />
                <span>Mentor is analyzing and preparing your answer...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Prompts */}
        <div className="px-4 py-2 bg-slate-50 border-t border-slate-100 flex items-center gap-2 overflow-x-auto text-xs">
          <span className="text-slate-400 shrink-0 font-semibold flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-indigo-500" /> Suggested:
          </span>
          {SUGGESTED_PROMPTS.map((prompt, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(prompt)}
              disabled={loading}
              className="shrink-0 px-2.5 py-1 bg-white hover:bg-indigo-50 text-slate-700 hover:text-indigo-700 border border-slate-200 hover:border-indigo-200 rounded-lg transition-colors cursor-pointer disabled:opacity-50"
            >
              {prompt}
            </button>
          ))}
        </div>

        {/* Chat Input Bar */}
        <div className="p-4 bg-white border-t border-slate-200">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-3"
          >
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask a question about mutual funds, SIP, emergency funds, or your spending..."
              disabled={loading}
              className="flex-1 px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl text-sm text-slate-900 placeholder-slate-400 focus:bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={!inputMessage.trim() || loading}
              className="px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition-colors disabled:opacity-50 flex items-center gap-2 cursor-pointer shadow-xs"
            >
              {loading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
              <span className="hidden sm:inline">Send</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AIMentor;
