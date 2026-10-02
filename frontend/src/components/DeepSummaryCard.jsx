import React, { useState } from 'react';
import { BookOpen, ChevronDown, ChevronUp, Copy, Check } from 'lucide-react';

export default function DeepSummaryCard({ summary, domain, title = "Comprehensive Executive Evaluation" }) {
  const [expanded, setExpanded] = useState(true);
  const [copied, setCopied] = useState(false);

  if (!summary) return null;

  const paragraphs = summary.split('\n\n').filter((p) => p.trim().length > 0);

  const handleCopy = () => {
    navigator.clipboard.writeText(summary);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white rounded-2xl p-6 mb-6 border border-slate-200 shadow-sm relative overflow-hidden">
      {/* Subtle top accent bar */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600" />

      <div className="flex items-center justify-between mb-3.5">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600 shrink-0">
            <BookOpen className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="text-base font-bold text-slate-900 tracking-tight">{title}</h3>
              <span className="px-2 py-0.5 text-[10px] font-extrabold uppercase rounded-full bg-blue-50 border border-blue-200 text-blue-700">
                In-Depth Analysis
              </span>
            </div>
            <p className="text-xs text-slate-500 font-medium">Exhaustive multi-tier synthesis grounded in document context</p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={handleCopy}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-slate-900 bg-slate-50 hover:bg-slate-100 border border-slate-200 transition shadow-xs"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
          <button
            onClick={() => setExpanded(!expanded)}
            className="p-1.5 rounded-lg text-slate-500 hover:text-slate-800 bg-slate-50 hover:bg-slate-100 border border-slate-200 transition shadow-xs"
          >
            {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {expanded && (
        <div className="space-y-3 text-xs text-slate-700 leading-relaxed pt-3 border-t border-slate-100">
          {paragraphs.map((para, index) => (
            <p key={index} className="text-justify leading-normal">
              {para}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}
