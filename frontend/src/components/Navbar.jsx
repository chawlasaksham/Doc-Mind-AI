import React from 'react';
import { Zap, Key, FileText, BarChart2, ShieldCheck, AlertCircle, Award } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, apiConfig, onOpenKeyModal }) {
  return (
    <header className="border-b border-slate-800/80 bg-dark-900/90 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Project Meta */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/25">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <span className="font-extrabold text-xl tracking-tight bg-gradient-to-r from-blue-400 via-indigo-300 to-purple-400 bg-clip-text text-transparent">
                    Doc–Mind AI
                  </span>
                  <span className="px-2 py-0.5 text-[10px] font-semibold bg-blue-500/10 border border-blue-500/20 text-blue-400 rounded-full">
                    v2.0
                  </span>
                </div>
                <p className="text-xs text-slate-400 hidden sm:block">Multi-Domain Document Intelligence & Dynamic Analytics</p>
              </div>
            </div>

            {/* JIIT Badge */}
            <div className="hidden lg:flex items-center pl-4 border-l border-slate-800 text-xs text-slate-400 space-x-2">
              <Award className="w-4 h-4 text-purple-400" />
              <span>JIIT Major Project (15B19CL791)</span>
            </div>
          </div>

          {/* Tab Navigation Controls */}
          <div className="flex items-center bg-dark-950 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setActiveTab('pdf')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${
                activeTab === 'pdf'
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-dark-850'
              }`}
            >
              <FileText className="w-4 h-4" />
              <span>PDF Intelligence</span>
            </button>
            <button
              onClick={() => setActiveTab('excel')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${
                activeTab === 'excel'
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-dark-850'
              }`}
            >
              <BarChart2 className="w-4 h-4" />
              <span>Excel & CSV Analytics</span>
            </button>
          </div>

          {/* Gemini API Key Button & Status */}
          <div className="flex items-center space-x-3">
            <button
              onClick={onOpenKeyModal}
              className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium border transition-all ${
                apiConfig.isConfigured
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/20'
                  : 'bg-amber-500/10 border-amber-500/30 text-amber-400 hover:bg-amber-500/20'
              }`}
            >
              <Key className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">
                {apiConfig.isConfigured ? 'Gemini Active' : 'Configure API Key'}
              </span>
              <span className="w-2 h-2 rounded-full animate-pulse bg-current"></span>
            </button>
          </div>

        </div>
      </div>
    </header>
  );
}
