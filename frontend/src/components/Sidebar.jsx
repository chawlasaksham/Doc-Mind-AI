import React from 'react';
import { Zap, FileText, BarChart2, Key, Users, Award, ShieldCheck } from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, apiConfig, onOpenKeyModal }) {
  const navItems = [
    {
      id: 'pdf',
      label: 'PDF Intelligence',
      sub: 'Multi-Domain Analytics & RAG',
      icon: FileText,
      activeColor: 'bg-blue-50 text-blue-700 border-blue-600',
      badgeColor: 'bg-blue-100 text-blue-700',
    },
    {
      id: 'excel',
      label: 'Excel Analytics',
      sub: 'Spreadsheets & Dynamic Charts',
      icon: BarChart2,
      activeColor: 'bg-emerald-50 text-emerald-700 border-emerald-600',
      badgeColor: 'bg-emerald-100 text-emerald-700',
    },
  ];

  return (
    <aside className="w-64 shrink-0 bg-white border-r border-slate-200 flex flex-col justify-between h-screen sticky top-0 shadow-sm select-none z-30">
      {/* Top: Branding & Title */}
      <div>
        <div className="p-5 border-b border-slate-100">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20 shrink-0">
              <Zap className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-lg tracking-tight text-slate-900">
                  Doc–Mind AI
                </span>
                <span className="px-1.5 py-0.5 text-[10px] font-bold bg-blue-50 text-blue-600 border border-blue-200 rounded-md">
                  v2.0
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium">Document Intelligence Platform</p>
            </div>
          </div>

          <div className="mt-3.5 px-3 py-2 rounded-lg bg-slate-50 border border-slate-100 flex items-center space-x-2 text-[11px] text-slate-600">
            <Award className="w-3.5 h-3.5 text-blue-600 shrink-0" />
            <span className="truncate font-medium">JIIT Major Project (15B19CL791)</span>
          </div>
        </div>

        {/* Navigation Tabs (Vertical on Left Side) */}
        <div className="p-3 space-y-1.5">
          <div className="px-3 pt-2 pb-1 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Navigation Tabs
          </div>

          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center space-x-3 px-3.5 py-3 rounded-xl text-left border transition-all ${
                  isActive
                    ? `${item.activeColor} border-l-4 font-bold shadow-sm`
                    : 'border-transparent text-slate-600 hover:text-slate-900 hover:bg-slate-50 font-semibold'
                }`}
              >
                <div className={`p-1.5 rounded-lg ${isActive ? 'bg-white shadow-xs' : 'text-slate-400'}`}>
                  <Icon className="w-4 h-4" />
                </div>
                <div className="truncate">
                  <div className="text-xs leading-tight">{item.label}</div>
                  <div className="text-[10px] text-slate-400 font-normal leading-tight mt-0.5">{item.sub}</div>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Bottom Section: API Key & Project Credits */}
      <div className="p-4 border-t border-slate-100 space-y-3 bg-slate-50/50">
        {/* Gemini API Key Trigger */}
        <button
          onClick={onOpenKeyModal}
          className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl border text-xs font-semibold transition ${
            apiConfig.isConfigured
              ? 'bg-emerald-50 border-emerald-200 text-emerald-700 hover:bg-emerald-100/70'
              : 'bg-amber-50 border-amber-200 text-amber-700 hover:bg-amber-100/70'
          }`}
        >
          <div className="flex items-center space-x-2">
            <Key className="w-3.5 h-3.5 shrink-0" />
            <span>{apiConfig.isConfigured ? 'Gemini API Active' : 'Configure API Key'}</span>
          </div>
          <span className={`w-2 h-2 rounded-full ${apiConfig.isConfigured ? 'bg-emerald-500' : 'bg-amber-500 animate-pulse'}`} />
        </button>

        {/* Project Team */}
        <div className="p-3 rounded-xl bg-white border border-slate-200/80 text-[11px] text-slate-600">
          <div className="flex items-center space-x-1.5 font-bold text-slate-800 mb-1">
            <Users className="w-3.5 h-3.5 text-blue-600" />
            <span>Project Team</span>
          </div>
          <p className="leading-snug text-slate-500">Saksham Chawla • Mrigank Rai • Aditya Kumar Gupta</p>
          <p className="text-[10px] text-slate-400 mt-0.5">Jaypee Institute of Information Technology</p>
        </div>
      </div>
    </aside>
  );
}
