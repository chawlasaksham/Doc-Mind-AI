import React, { useState, useRef } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend,
  LineChart, Line, ScatterChart, Scatter, AreaChart, Area, Cell
} from 'recharts';
import {
  Table, UploadCloud, FileSpreadsheet, Sparkles, TrendingUp, AlertTriangle,
  Lightbulb, Download, CheckCircle2, ChevronDown, Loader2
} from 'lucide-react';
import DeepSummaryCard from './DeepSummaryCard';

export default function ExcelDashboard({
  excelData, onFileUpload, isUploading, onSheetChange
}) {
  const fileInputRef = useRef(null);

  // Custom Chart Studio state
  const [chartType, setChartType] = useState('Bar');
  const [xAxisCol, setXAxisCol] = useState('');
  const [yAxisCol, setYAxisCol] = useState('');

  const profile = excelData?.profile || {};
  const chartPayload = excelData?.chart_payload || {};
  const aiStory = excelData?.ai_story || {};
  const previewRows = excelData?.preview_rows || [];

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileUpload(e.target.files[0]);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Upload Zone (Light Theme) */}
      <div
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-2xl p-7 text-center cursor-pointer transition-all duration-200 ${
          isUploading
            ? 'border-emerald-400 bg-emerald-50/50'
            : 'border-slate-300 hover:border-emerald-500 bg-white hover:bg-slate-50/80 shadow-xs'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".xlsx,.xls,.csv"
          onChange={handleFileChange}
          className="hidden"
        />
        <div className="flex flex-col items-center justify-center space-y-2.5">
          <div className="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600 shadow-sm">
            {isUploading ? <Loader2 className="w-6 h-6 animate-spin text-emerald-600" /> : <FileSpreadsheet className="w-6 h-6" />}
          </div>
          <div>
            <h4 className="text-sm font-bold text-slate-900">
              {isUploading ? 'Ingesting Spreadsheet & Calculating Statistical Profile...' : 'Upload Excel (.xlsx, .xls) or CSV Spreadsheet'}
            </h4>
            <p className="text-xs text-slate-500 mt-0.5">
              Supports multi-sheet workbooks, automated schema profiling, distributions, and AI data story synthesis
            </p>
          </div>
          {excelData && !isUploading && (
            <div className="flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              <span>Loaded: {excelData.filename} ({profile.total_rows?.toLocaleString()} rows, {profile.total_cols} columns)</span>
            </div>
          )}
        </div>
      </div>

      {excelData && (
        <>
          {/* Worksheet Selector if multi-sheet */}
          {excelData.sheets && excelData.sheets.length > 1 && (
            <div className="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm flex items-center justify-between">
              <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">Active Worksheet:</span>
              <div className="flex items-center space-x-2">
                {excelData.sheets.map((sheet) => (
                  <button
                    key={sheet}
                    onClick={() => onSheetChange(sheet)}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition ${
                      excelData.active_sheet === sheet
                        ? 'bg-emerald-600 text-white shadow-xs'
                        : 'bg-slate-100 text-slate-600 hover:text-slate-900 hover:bg-slate-200'
                    }`}
                  >
                    {sheet}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Statistical Health Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard title="Total Records" value={(profile.total_rows || 0).toLocaleString()} sub="Data Rows" color="text-emerald-700" bg="bg-emerald-50" />
            <StatCard title="Feature Columns" value={profile.total_cols || 0} sub={`${profile.numeric_cols?.length || 0} Numeric, ${profile.categorical_cols?.length || 0} Categorical`} color="text-blue-700" bg="bg-blue-50" />
            <StatCard title="Data Completeness" value={`${(100 - (profile.missing_pct || 0)).toFixed(1)}%`} sub={`${profile.missing_count || 0} Missing Cells`} color="text-purple-700" bg="bg-purple-50" />
            <StatCard title="Continuous Metrics" value={profile.numeric_cols?.length || 0} sub="Quantitative Features" color="text-amber-700" bg="bg-amber-50" />
          </div>

          {/* Deep AI Data Story & Executive Synthesis */}
          <DeepSummaryCard
            summary={aiStory.executive_summary}
            domain="Excel Analytics"
            title="Comprehensive Commercial Data Story & Analytical Narrative"
          />

          {/* Automated Recharts Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Distribution */}
            {chartPayload.distribution && (
              <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-4">
                  Parametric Distribution: {chartPayload.distribution.column}
                </h4>
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartPayload.distribution.data}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                      <XAxis dataKey="bin" tick={{ fill: '#64748B', fontSize: 10 }} />
                      <YAxis tick={{ fill: '#64748B', fontSize: 10 }} />
                      <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px' }} />
                      <Bar dataKey="count" fill="#059669" radius={[6, 6, 0, 0]} name="Frequency" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {/* Categorical Breakdown */}
            {chartPayload.categorical && (
              <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-4">
                  Segment Breakdown: {chartPayload.categorical.column}
                </h4>
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartPayload.categorical.data} layout="vertical" margin={{ top: 5, right: 20, left: 35, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                      <XAxis type="number" tick={{ fill: '#64748B', fontSize: 10 }} />
                      <YAxis dataKey="category" type="category" tick={{ fill: '#64748B', fontSize: 10 }} />
                      <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px' }} />
                      <Bar dataKey="count" fill="#2563EB" radius={[0, 6, 6, 0]} name="Transactions" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {/* Longitudinal Trend Area */}
            {chartPayload.trend && (
              <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm lg:col-span-2">
                <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-4">
                  Multi-Period Longitudinal Trend: {chartPayload.trend.num_col}
                </h4>
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartPayload.trend.data}>
                      <defs>
                        <linearGradient id="colorTrendLight" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#7C3AED" stopOpacity={0.25} />
                          <stop offset="95%" stopColor="#7C3AED" stopOpacity={0.0} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                      <XAxis dataKey="date" tick={{ fill: '#64748B', fontSize: 10 }} />
                      <YAxis tick={{ fill: '#64748B', fontSize: 10 }} />
                      <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px' }} />
                      <Area type="monotone" dataKey="value" stroke="#7C3AED" strokeWidth={2} fillOpacity={1} fill="url(#colorTrendLight)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}
          </div>

          {/* AI Insights: Patterns, Risks, Recommendations */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm border-l-4 border-l-blue-600">
              <div className="flex items-center space-x-2 text-blue-700 mb-3">
                <TrendingUp className="w-4 h-4" />
                <h4 className="font-bold text-xs uppercase tracking-wider">Key Observed Patterns</h4>
              </div>
              <ul className="space-y-2 text-xs text-slate-600 leading-relaxed">
                {(aiStory.key_patterns || []).map((p, i) => (
                  <li key={i} className="flex items-start space-x-1.5">
                    <span className="text-blue-600 font-bold">•</span>
                    <span>{p}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm border-l-4 border-l-amber-500">
              <div className="flex items-center space-x-2 text-amber-700 mb-3">
                <AlertTriangle className="w-4 h-4" />
                <h4 className="font-bold text-xs uppercase tracking-wider">Data Hygiene & Risk Audit</h4>
              </div>
              <ul className="space-y-2 text-xs text-slate-600 leading-relaxed">
                {(aiStory.anomalies_or_risks || []).map((a, i) => (
                  <li key={i} className="flex items-start space-x-1.5">
                    <span className="text-amber-600 font-bold">•</span>
                    <span>{a}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm border-l-4 border-l-emerald-600">
              <div className="flex items-center space-x-2 text-emerald-700 mb-3">
                <Lightbulb className="w-4 h-4" />
                <h4 className="font-bold text-xs uppercase tracking-wider">Strategic Recommendations</h4>
              </div>
              <ul className="space-y-2 text-xs text-slate-600 leading-relaxed">
                {(aiStory.actionable_recommendations || []).map((r, i) => (
                  <li key={i} className="flex items-start space-x-1.5">
                    <span className="text-emerald-600 font-bold">•</span>
                    <span>{r}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Raw Data Preview Table */}
          <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                Raw Data Sample (First 30 Records)
              </h4>
              <button
                onClick={() => {
                  const headers = Object.keys(previewRows[0] || {}).join(',');
                  const rows = previewRows.map(r => Object.values(r).join(',')).join('\n');
                  const blob = new Blob([`${headers}\n${rows}`], { type: 'text/csv' });
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement('a');
                  a.href = url;
                  a.download = `export_${excelData.filename}.csv`;
                  a.click();
                }}
                className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-50 border border-slate-200 text-xs font-semibold text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition shadow-xs"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Export CSV</span>
              </button>
            </div>
            <div className="overflow-x-auto max-h-72">
              <table className="w-full text-left text-xs text-slate-700">
                <thead className="bg-slate-50 text-slate-600 uppercase tracking-wider sticky top-0 border-b border-slate-200">
                  <tr>
                    {Object.keys(previewRows[0] || {}).map((h) => (
                      <th key={h} className="p-2.5 whitespace-nowrap font-bold">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {previewRows.map((r, idx) => (
                    <tr key={idx} className="hover:bg-slate-50/80">
                      {Object.values(r).map((v, cIdx) => (
                        <td key={cIdx} className="p-2.5 whitespace-nowrap">{String(v)}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

function StatCard({ title, value, sub, color = 'text-emerald-700', bg = 'bg-emerald-50' }) {
  return (
    <div className="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm">
      <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block truncate">{title}</span>
      <span className={`text-xl font-extrabold block truncate my-1 ${color}`}>{value}</span>
      <span className="text-[11px] text-slate-500 block truncate">{sub}</span>
    </div>
  );
}
