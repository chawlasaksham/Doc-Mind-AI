import React from 'react';
import { GraduationCap, Microscope, Stethoscope, Table, Sparkles } from 'lucide-react';

export default function SampleBar({ onLoadSample, loading }) {
  const samples = [
    {
      id: 'marksheet',
      type: 'pdf',
      label: 'Academic Marksheet',
      sub: 'Education Domain',
      icon: GraduationCap,
      color: 'from-blue-600 to-indigo-600',
      border: 'border-blue-500/30',
      text: 'text-blue-400',
    },
    {
      id: 'research',
      type: 'pdf',
      label: 'Research Paper',
      sub: 'Research Domain',
      icon: Microscope,
      color: 'from-purple-600 to-indigo-600',
      border: 'border-purple-500/30',
      text: 'text-purple-400',
    },
    {
      id: 'healthcare',
      type: 'pdf',
      label: 'Clinical Lab Report',
      sub: 'Healthcare Domain',
      icon: Stethoscope,
      color: 'from-emerald-600 to-teal-600',
      border: 'border-emerald-500/30',
      text: 'text-emerald-400',
    },
    {
      id: 'sales',
      type: 'excel',
      label: 'Sales Performance CSV',
      sub: 'Multi-Sheet Analytics',
      icon: Table,
      color: 'from-amber-600 to-orange-600',
      border: 'border-amber-500/30',
      text: 'text-amber-400',
    },
  ];

  return (
    <div className="bg-dark-900/60 border border-slate-800/80 rounded-2xl p-3 mb-6 flex flex-wrap items-center justify-between gap-3">
      <div className="flex items-center space-x-2 pl-2">
        <Sparkles className="w-4 h-4 text-amber-400 animate-pulse" />
        <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
          Instant 1-Click Demos:
        </span>
      </div>

      <div className="flex flex-wrap items-center gap-2">
        {samples.map((s) => {
          const Icon = s.icon;
          return (
            <button
              key={s.id}
              onClick={() => onLoadSample(s.id, s.type)}
              disabled={loading}
              className={`flex items-center space-x-2 px-3 py-1.5 rounded-xl border ${s.border} bg-dark-950/80 hover:bg-dark-850 hover:scale-[1.02] transition-all text-xs font-semibold disabled:opacity-50`}
            >
              <div className={`w-5 h-5 rounded-md bg-gradient-to-tr ${s.color} flex items-center justify-center text-white shrink-0`}>
                <Icon className="w-3 h-3" />
              </div>
              <div className="text-left">
                <span className="text-slate-200 block leading-tight">{s.label}</span>
                <span className={`text-[10px] block leading-tight ${s.text}`}>{s.sub}</span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
