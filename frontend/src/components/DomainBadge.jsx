import React from 'react';
import { GraduationCap, Microscope, Stethoscope, Briefcase, FileText, ChevronDown } from 'lucide-react';

const DOMAIN_STYLES = {
  Education: {
    icon: GraduationCap,
    gradient: 'from-blue-600 to-indigo-600',
    border: 'border-blue-200',
    bg: 'bg-blue-50',
    text: 'text-blue-700',
    badge: 'bg-blue-100 text-blue-800',
  },
  Research: {
    icon: Microscope,
    gradient: 'from-purple-600 to-indigo-600',
    border: 'border-purple-200',
    bg: 'bg-purple-50',
    text: 'text-purple-700',
    badge: 'bg-purple-100 text-purple-800',
  },
  Healthcare: {
    icon: Stethoscope,
    gradient: 'from-emerald-600 to-teal-600',
    border: 'border-emerald-200',
    bg: 'bg-emerald-50',
    text: 'text-emerald-700',
    badge: 'bg-emerald-100 text-emerald-800',
  },
  Finance: {
    icon: Briefcase,
    gradient: 'from-amber-600 to-orange-600',
    border: 'border-amber-200',
    bg: 'bg-amber-50',
    text: 'text-amber-700',
    badge: 'bg-amber-100 text-amber-800',
  },
  'General / Business': {
    icon: FileText,
    gradient: 'from-indigo-600 to-blue-600',
    border: 'border-indigo-200',
    bg: 'bg-indigo-50',
    text: 'text-indigo-700',
    badge: 'bg-indigo-100 text-indigo-800',
  },
};

export default function DomainBadge({ domain, confidence, subCategory, rationale, onOverrideDomain }) {
  const meta = DOMAIN_STYLES[domain] || DOMAIN_STYLES['General / Business'];
  const Icon = meta.icon;
  const pct = Math.round((confidence || 0.95) * 100);

  const domainOptions = ['Education', 'Research', 'Healthcare', 'Finance', 'General / Business'];

  return (
    <div className="bg-white rounded-2xl p-5 mb-6 border border-slate-200 shadow-sm">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        
        {/* Left: Domain Indicator */}
        <div className="flex items-center space-x-4">
          <div className={`w-13 h-13 rounded-2xl bg-gradient-to-tr ${meta.gradient} flex items-center justify-center text-white shadow-md shrink-0 p-3`}>
            <Icon className="w-7 h-7" />
          </div>

          <div>
            <div className="flex items-center space-x-2.5">
              <span className="text-[11px] uppercase tracking-wider text-slate-400 font-bold">
                Identified Domain
              </span>
              <span className={`px-2 py-0.5 rounded-full text-[11px] font-extrabold ${meta.badge}`}>
                {pct}% Confidence
              </span>
            </div>

            <div className="flex items-center space-x-2 mt-0.5">
              <h2 className="text-xl font-extrabold tracking-tight text-slate-900">{domain}</h2>
              {subCategory && (
                <span className="text-xs font-semibold text-slate-500">
                  ({subCategory})
                </span>
              )}
            </div>

            {rationale && (
              <p className="text-xs text-slate-500 mt-1 max-w-2xl leading-relaxed">
                <strong className="text-slate-700 font-semibold">Agent Rationale:</strong> {rationale}
              </p>
            )}
          </div>
        </div>

        {/* Right: Manual Override Dropdown */}
        <div className="flex items-center space-x-2.5 bg-slate-50 p-2 rounded-xl border border-slate-200 self-start md:self-auto shrink-0">
          <span className="text-xs font-semibold text-slate-600 pl-1">Override Domain:</span>
          <div className="relative">
            <select
              value={domain}
              onChange={(e) => onOverrideDomain(e.target.value)}
              className="bg-white border border-slate-300 rounded-lg px-3 py-1.5 text-xs font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500 pr-7 appearance-none cursor-pointer shadow-xs"
            >
              {domainOptions.map((opt) => (
                <option key={opt} value={opt}>
                  {opt}
                </option>
              ))}
            </select>
            <ChevronDown className="w-3.5 h-3.5 text-slate-500 absolute right-2 top-2.5 pointer-events-none" />
          </div>
        </div>

      </div>
    </div>
  );
}
