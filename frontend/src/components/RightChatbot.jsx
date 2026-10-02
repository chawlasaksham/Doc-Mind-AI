import React, { useState, useRef, useEffect } from 'react';
import {
  MessageSquare, Send, Bot, User, Sparkles, FileText,
  ChevronDown, ChevronUp, Trash2, Maximize2, Minimize2, Loader2
} from 'lucide-react';

export default function RightChatbot({
  activeTab,
  pdfChatHistory,
  onSendPdfQuery,
  isPdfChatting,
  domain,
  excelChatHistory,
  onSendExcelQuery,
  isExcelChatting,
  aiStory,
  onClearChat,
}) {
  const [input, setInput] = useState('');
  const [isCollapsed, setIsCollapsed] = useState(false);
  const messagesEndRef = useRef(null);

  const isPdf = activeTab === 'pdf';
  const chatHistory = isPdf ? pdfChatHistory : excelChatHistory;
  const isChatting = isPdf ? isPdfChatting : isExcelChatting;
  const onSendMessage = isPdf ? onSendPdfQuery : onSendExcelQuery;

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

  // Dynamic suggested prompts
  const pdfDomainPrompts = {
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

  const hasDocument = isPdf ? Boolean(domain) : Boolean(aiStory);

  const promptChips = isPdf
    ? (domain ? (pdfDomainPrompts[domain] || pdfDomainPrompts['General / Business']) : [])
    : (aiStory?.suggested_questions || []);

  if (isCollapsed) {
    return (
      <div className="fixed bottom-6 right-6 z-30">
        <button
          onClick={() => setIsCollapsed(false)}
          className="flex items-center space-x-2 px-4 py-3 rounded-2xl bg-blue-600 hover:bg-blue-700 text-white font-bold shadow-lg shadow-blue-500/30 transition transform hover:scale-105"
        >
          <MessageSquare className="w-5 h-5" />
          <span className="text-xs">Open {isPdf ? 'Document' : 'Data'} Chatbot</span>
        </button>
      </div>
    );
  }

  return (
    <aside className="w-96 shrink-0 bg-white border-l border-slate-200 flex flex-col h-screen sticky top-0 shadow-sm z-20">
      {/* Header */}
      <div className="p-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/70">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-sm shadow-blue-500/20 shrink-0">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-xs font-bold text-slate-900 leading-tight">
              {isPdf ? 'Doc-Mind AI RAG Chat' : 'AI Data Analyst'}
            </h3>
            <p className="text-[10px] text-slate-500">
              {isPdf ? 'Context Grounded Search' : 'Spreadsheet Intelligence'}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-1">
          <button
            onClick={onClearChat}
            title="Clear Chat History"
            className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
          <button
            onClick={() => setIsCollapsed(true)}
            title="Minimize"
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition"
          >
            <Minimize2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Suggested Prompt Chips */}
      {hasDocument && promptChips.length > 0 && (
        <div className="p-3 bg-slate-50 border-b border-slate-100 space-y-1.5">
          <div className="flex items-center space-x-1.5 text-[10px] font-bold uppercase tracking-wider text-slate-500">
            <Sparkles className="w-3 h-3 text-amber-500" />
            <span>Suggested Questions:</span>
          </div>
          <div className="flex flex-col gap-1">
            {promptChips.slice(0, 3).map((chip, idx) => (
              <button
                key={idx}
                onClick={() => onSendMessage(chip)}
                disabled={isChatting}
                className="text-left px-2.5 py-1.5 rounded-lg text-[11px] font-medium bg-white hover:bg-blue-50 text-slate-700 hover:text-blue-700 border border-slate-200/80 hover:border-blue-300 transition truncate shadow-xs disabled:opacity-50"
              >
                • {chip}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3.5">
        {chatHistory.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center text-slate-400 px-4 space-y-2">
            <MessageSquare className="w-8 h-8 text-slate-300" />
            <p className="text-xs font-medium text-slate-600">
              {isPdf
                ? (domain ? `Ready to discuss ${domain} document.` : 'Awaiting PDF upload.')
                : (aiStory ? 'Ready to analyze spreadsheet.' : 'Awaiting spreadsheet upload.')}
            </p>
            <p className="text-[11px] text-slate-400 leading-snug">
              {isPdf
                ? (domain
                    ? 'Answers are grounded in vector chunks with explicit page references.'
                    : 'Upload a PDF in the main panel to begin asking grounded questions.')
                : (aiStory
                    ? 'Calculates totals, averages, rankings, and statistical distributions.'
                    : 'Upload an Excel or CSV file to query statistical calculations.')}
            </p>
          </div>
        ) : (
          chatHistory.map((msg, idx) => (
            <div
              key={idx}
              className={`flex items-start space-x-2 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.role !== 'user' && (
                <div className="w-6 h-6 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center text-[10px] font-bold shrink-0 mt-0.5">
                  AI
                </div>
              )}

              <div
                className={`max-w-[85%] rounded-2xl px-3.5 py-2.5 text-xs leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white shadow-sm shadow-blue-500/20'
                    : 'bg-white border border-slate-200 text-slate-800 shadow-xs'
                }`}
              >
                <div className="whitespace-pre-wrap">{msg.content}</div>

                {/* Retrieved chunks expander (for PDF RAG) */}
                {msg.retrieved_chunks && msg.retrieved_chunks.length > 0 && (
                  <EvidenceExpander chunks={msg.retrieved_chunks} />
                )}
              </div>

              {msg.role === 'user' && (
                <div className="w-6 h-6 rounded-lg bg-slate-200 text-slate-700 flex items-center justify-center text-[10px] font-bold shrink-0 mt-0.5">
                  You
                </div>
              )}
            </div>
          ))
        )}

        {isChatting && (
          <div className="flex items-center space-x-2 text-xs text-slate-500 py-1">
            <Loader2 className="w-4 h-4 animate-spin text-blue-600" />
            <span>Analyzing context & synthesizing answer...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="p-3 border-t border-slate-200 bg-white">
        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={
              isPdf
                ? (domain ? "Ask about the PDF document..." : "Upload a PDF first to ask questions...")
                : (aiStory ? "Ask about the spreadsheet..." : "Upload a spreadsheet first to ask questions...")
            }
            disabled={isChatting || !hasDocument}
            className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={!input.trim() || isChatting || !hasDocument}
            className="p-2 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-40 text-white transition shadow-sm"
          >
            <Send className="w-3.5 h-3.5" />
          </button>
        </form>
        <p className="text-[10px] text-slate-400 text-center mt-1.5">
          Grounded with Google Gemini API & Vector RAG
        </p>
      </div>
    </aside>
  );
}

function EvidenceExpander({ chunks }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="mt-2.5 pt-2 border-t border-slate-100">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center space-x-1 text-[10px] font-bold text-blue-600 hover:text-blue-700 transition"
      >
        <FileText className="w-3 h-3" />
        <span>{open ? 'Hide Sources' : `View ${chunks.length} Grounded Excerpts`}</span>
        {open ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
      </button>

      {open && (
        <div className="mt-1.5 space-y-1.5">
          {chunks.map((chk, i) => (
            <div key={i} className="p-2 rounded-lg bg-slate-50 border border-slate-200 text-[10px] text-slate-600">
              <div className="flex items-center justify-between font-bold text-slate-700 mb-0.5">
                <span>Page {chk.page || 'N/A'}</span>
                <span className="text-emerald-600">{Math.round((chk.similarity_score || 0) * 100)}% Match</span>
              </div>
              <p className="italic leading-snug">"{chk.text?.slice(0, 180)}..."</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
