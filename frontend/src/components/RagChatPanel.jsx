import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, Send, Sparkles, User, Bot, ChevronDown, ChevronUp, FileText, Loader2 } from 'lucide-react';

export default function RagChatPanel({ chatHistory, onSendMessage, isChatting, domain }) {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory, isChatting]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isChatting) return;
    onSendMessage(input.trim());
    setInput('');
  };

  const domainPrompts = {
    Education: [
      "What is the student's highest scoring subject?",
      "Summarize the academic weaknesses and study recommendations.",
      "What is the overall percentage and GPA?"
    ],
    Research: [
      "What is the core research objective and methodology?",
      "How do experimental metrics compare to the baseline?",
      "What are the major limitations and future scope?"
    ],
    Healthcare: [
      "Which biomarkers were flagged outside standard reference ranges?",
      "What are the key questions to discuss with the doctor?",
      "Explain the clinical significance of the elevated glucose."
    ],
    Finance: [
      "What is the net profit margin and total revenue?",
      "Break down the primary operating expenses.",
      "What are the key financial risk factors?"
    ],
    'General / Business': [
      "Provide an executive summary of this document.",
      "What are the key action items and owners?",
      "Who are the main organizations and people mentioned?"
    ]
  };

  const promptChips = domainPrompts[domain] || domainPrompts['General / Business'];

  return (
    <div className="glass-panel rounded-2xl border border-slate-700/80 shadow-2xl p-6 mt-8">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-blue-400">
            <MessageSquare className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-white tracking-tight">
              Interactive Document Chatbot (Doc-Mind AI RAG)
            </h3>
            <p className="text-xs text-slate-400">
              Grounded in document context using vector semantic search
            </p>
          </div>
        </div>
      </div>

      {/* Suggested Chips */}
      <div className="py-3 flex flex-wrap items-center gap-2 border-b border-slate-800/60">
        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider flex items-center space-x-1 mr-1">
          <Sparkles className="w-3 h-3 text-amber-400" />
          <span>Suggested:</span>
        </span>
        {promptChips.map((chip, idx) => (
          <button
            key={idx}
            onClick={() => onSendMessage(chip)}
            disabled={isChatting}
            className="px-3 py-1 rounded-full text-xs font-medium bg-dark-900 border border-slate-800 hover:border-blue-500/40 text-slate-300 hover:text-white transition disabled:opacity-50 text-left"
          >
            {chip}
          </button>
        ))}
      </div>

      {/* Message Stream */}
      <div className="h-80 overflow-y-auto py-4 space-y-4 pr-1">
        {chatHistory.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-slate-500 text-xs text-center space-y-2">
            <Bot className="w-8 h-8 text-slate-600" />
            <p>Ask any question about this document.<br />Grounded answers will cite exact pages and sections.</p>
          </div>
        ) : (
          chatHistory.map((msg, idx) => (
            <div
              key={idx}
              className={`flex items-start space-x-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.role !== 'user' && (
                <div className="w-8 h-8 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400 shrink-0 mt-0.5">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div
                className={`max-w-2xl rounded-2xl p-4 text-xs leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/20'
                    : 'bg-dark-900/90 border border-slate-800 text-slate-200'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>

                {/* Retrieved context chunks citations */}
                {msg.retrieved_chunks && msg.retrieved_chunks.length > 0 && (
                  <EvidenceExpander chunks={msg.retrieved_chunks} />
                )}
              </div>

              {msg.role === 'user' && (
                <div className="w-8 h-8 rounded-xl bg-slate-800 flex items-center justify-center text-slate-300 shrink-0 mt-0.5">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          ))
        )}

        {isChatting && (
          <div className="flex items-center space-x-3 text-xs text-slate-400">
            <div className="w-8 h-8 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
              <Loader2 className="w-4 h-4 animate-spin" />
            </div>
            <span>Retrieving document evidence & synthesizing grounded answer...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Box */}
      <form onSubmit={handleSubmit} className="pt-3 border-t border-slate-800 flex items-center space-x-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask any question about this document..."
          disabled={isChatting}
          className="flex-1 bg-dark-900 border border-slate-700/80 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
        />
        <button
          type="submit"
          disabled={!input.trim() || isChatting}
          className="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-bold transition shadow-lg shadow-blue-600/20 flex items-center justify-center"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}

function EvidenceExpander({ chunks }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="mt-3 pt-2 border-t border-slate-800">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center space-x-1.5 text-[11px] font-semibold text-blue-400 hover:text-blue-300 transition"
      >
        <FileText className="w-3.5 h-3.5" />
        <span>{open ? 'Hide Document Evidence' : `View ${chunks.length} Grounded Evidence Chunks`}</span>
        {open ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
      </button>

      {open && (
        <div className="mt-2 space-y-2">
          {chunks.map((chk, i) => (
            <div key={i} className="p-2.5 rounded-lg bg-dark-950 border border-slate-800 text-[11px] text-slate-300">
              <div className="flex items-center justify-between text-slate-400 font-bold mb-1">
                <span>Page {chk.page || 'N/A'}</span>
                <span className="text-emerald-400">Similarity: {Math.round((chk.similarity_score || 0) * 100)}%</span>
              </div>
              <p className="italic text-slate-400 leading-snug">"{chk.text?.slice(0, 240)}..."</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
