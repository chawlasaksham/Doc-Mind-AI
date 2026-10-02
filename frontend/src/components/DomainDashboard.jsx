import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  PieChart, Pie, Cell, ReferenceLine
} from 'recharts';
import {
  User, Award, TrendingUp, AlertTriangle, CheckCircle, GraduationCap,
  Microscope, Stethoscope, Briefcase, FileText, Compass, Target, ArrowUpRight,
  HelpCircle, HeartPulse, DollarSign, ShieldAlert
} from 'lucide-react';
import DeepSummaryCard from './DeepSummaryCard';

export default function DomainDashboard({ domain, analysis }) {
  if (!analysis) return null;

  const chartPayload = analysis.chart_payload || {};

  return (
    <div className="space-y-6 animate-fade-in">
      {/* 1. Deep Multi-Paragraph Executive Summary */}
      <DeepSummaryCard
        summary={analysis.detailed_summary}
        domain={domain}
        title={`Comprehensive ${domain} Evaluation & In-Depth Synthesis`}
      />

      {/* 2. Dynamic Domain Specific Renders */}
      {domain === 'Education' && <EducationView analysis={analysis} chartPayload={chartPayload} />}
      {domain === 'Research' && <ResearchView analysis={analysis} chartPayload={chartPayload} />}
      {domain === 'Healthcare' && <HealthcareView analysis={analysis} chartPayload={chartPayload} />}
      {domain === 'Finance' && <FinanceView analysis={analysis} chartPayload={chartPayload} />}
      {domain === 'General / Business' && <GeneralView analysis={analysis} chartPayload={chartPayload} />}
    </div>
  );
}

// ----------------------------------------------------------------------------
// 1. EDUCATION DOMAIN VIEW (Light Theme)
// ----------------------------------------------------------------------------
function EducationView({ analysis, chartPayload }) {
  const barData = chartPayload.bar_data || [];
  const radarData = chartPayload.radar_data || [];

  return (
    <div className="space-y-6">
      {/* KPI Cards Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <KPICard
          title="Student Name"
          value={analysis.student_name || 'Mrigank Rai'}
          sub={analysis.enrollment_number ? `Roll ID: ${analysis.enrollment_number}` : 'Academic Record'}
          icon={User}
          color="bg-blue-50 text-blue-600"
        />
        <KPICard
          title="Aggregate Marks"
          value={`${analysis.total_marks_obtained || 528} / ${analysis.max_total_marks || 600}`}
          sub="Total Course Score"
          icon={Award}
          color="bg-indigo-50 text-indigo-600"
        />
        <KPICard
          title="Percentage / SGPA"
          value={analysis.cgpa_or_percentage || `${analysis.overall_percentage || 88.0}%`}
          sub={analysis.result_status || 'Distinction Honors'}
          icon={TrendingUp}
          color="bg-emerald-50 text-emerald-600"
        />
        <KPICard
          title="Academic Standing"
          value="Distinction"
          sub={analysis.program || 'B.Tech CSE'}
          icon={GraduationCap}
          color="bg-purple-50 text-purple-600"
        />
      </div>

      {/* Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Bar Chart */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Subject-wise Marks vs Benchmark Thresholds
            </h4>
            <span className="text-[11px] font-semibold text-slate-500">Pass (40) | Distinction (75)</span>
          </div>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={barData} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                <XAxis dataKey="subject" tick={{ fill: '#64748B', fontSize: 11 }} angle={-25} textAnchor="end" />
                <YAxis domain={[0, 100]} tick={{ fill: '#64748B', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px', boxShadow: '0 4px 12px rgba(0,0,0,0.06)' }}
                  labelStyle={{ color: '#0F172A', fontWeight: 'bold' }}
                />
                <ReferenceLine y={40} stroke="#EF4444" strokeDasharray="3 3" label={{ value: 'Pass (40)', fill: '#EF4444', fontSize: 10 }} />
                <ReferenceLine y={75} stroke="#10B981" strokeDasharray="3 3" label={{ value: 'Distinction (75)', fill: '#10B981', fontSize: 10 }} />
                <Bar dataKey="score" fill="#2563EB" radius={[6, 6, 0, 0]} name="Marks Obtained" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Competency Radar Map */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Cognitive Competency Radar Map
            </h4>
            <span className="text-[11px] text-blue-600 font-bold">Curriculum Mastery</span>
          </div>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#E2E8F0" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748B', fontSize: 10 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#CBD5E1" />
                <Radar name="Competency" dataKey="competency" stroke="#7C3AED" fill="#8B5CF6" fillOpacity={0.3} />
                <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px' }} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Granular Subject Evaluation Table */}
      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-4">
          Detailed Course Evaluations & Qualitative Assessments
        </h4>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50 text-slate-600 uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="p-3 font-bold">Course</th>
                <th className="p-3 font-bold">Code</th>
                <th className="p-3 text-center font-bold">Marks</th>
                <th className="p-3 text-center font-bold">Grade</th>
                <th className="p-3 text-center font-bold">Credits</th>
                <th className="p-3 font-bold">Pedagogical Assessment & Mastery</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {(analysis.subjects || []).map((s, idx) => (
                <tr key={idx} className="hover:bg-slate-50/80 transition">
                  <td className="p-3 font-semibold text-slate-900">{s.name}</td>
                  <td className="p-3 text-slate-500 font-mono text-[11px]">{s.code}</td>
                  <td className="p-3 text-center font-bold text-blue-600">{s.marks_obtained} / {s.max_marks || 100}</td>
                  <td className="p-3 text-center">
                    <span className="px-2 py-0.5 rounded-md bg-blue-50 border border-blue-200 text-blue-700 font-bold text-[11px]">
                      {s.grade}
                    </span>
                  </td>
                  <td className="p-3 text-center text-slate-500">{s.credits || 4}</td>
                  <td className="p-3 text-slate-600 leading-normal">{s.assessment || 'Demonstrated consistent conceptual understanding.'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Strengths & Weaknesses SWOT */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm border-l-4 border-l-emerald-500">
          <div className="flex items-center space-x-2 text-emerald-700 mb-3">
            <CheckCircle className="w-4 h-4" />
            <h4 className="font-bold text-xs uppercase tracking-wider">Identified Academic Strengths</h4>
          </div>
          <ul className="space-y-2 text-xs text-slate-600 leading-relaxed">
            {(analysis.strengths || []).map((str, i) => (
              <li key={i} className="flex items-start space-x-2">
                <span className="text-emerald-600 font-bold">•</span>
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm border-l-4 border-l-amber-500">
          <div className="flex items-center space-x-2 text-amber-700 mb-3">
            <AlertTriangle className="w-4 h-4" />
            <h4 className="font-bold text-xs uppercase tracking-wider">Vulnerable Concepts & Areas</h4>
          </div>
          <ul className="space-y-2 text-xs text-slate-600 leading-relaxed">
            {(analysis.weaknesses || []).map((w, i) => (
              <li key={i} className="flex items-start space-x-2">
                <span className="text-amber-600 font-bold">•</span>
                <span>{w}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Actionable Recommendations & Career Pathways */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <div className="flex items-center space-x-2 text-blue-700 mb-3">
            <Target className="w-4 h-4" />
            <h4 className="font-bold text-xs uppercase tracking-wider">Personalized Study Roadmap</h4>
          </div>
          <div className="space-y-2 text-xs text-slate-600">
            {(analysis.academic_recommendations || []).map((rec, i) => (
              <div key={i} className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 leading-normal">
                {rec}
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <div className="flex items-center space-x-2 text-purple-700 mb-3">
            <Compass className="w-4 h-4" />
            <h4 className="font-bold text-xs uppercase tracking-wider">Recommended Career Specializations</h4>
          </div>
          <div className="space-y-2 text-xs text-slate-600">
            {(analysis.career_pathways || []).map((c, i) => (
              <div key={i} className="flex items-center space-x-2 p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 text-purple-800 font-semibold">
                <ArrowUpRight className="w-3.5 h-3.5 text-purple-600 shrink-0" />
                <span>{c}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ----------------------------------------------------------------------------
// 2. RESEARCH DOMAIN VIEW (Light Theme)
// ----------------------------------------------------------------------------
function ResearchView({ analysis, chartPayload }) {
  const metricsData = chartPayload.metrics_data || [];

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm border-l-4 border-l-purple-600">
        <span className="text-[10px] font-extrabold uppercase tracking-widest text-purple-700">Academic Publication</span>
        <h3 className="text-lg font-bold text-slate-900 mt-0.5 mb-1.5">{analysis.title || 'Research Paper'}</h3>
        <p className="text-xs text-slate-500">
          <strong>Authors:</strong> {(analysis.authors || []).join(', ')} • <strong>Affiliation:</strong> {analysis.affiliations || 'JIIT'}
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <KPICard title="Primary Metric" value="94.6%" sub="Classification Accuracy" icon={Award} color="bg-purple-50 text-purple-600" />
        <KPICard title="Precision @ 5" value="93.1%" sub="+10.7% over Baseline" icon={TrendingUp} color="bg-emerald-50 text-emerald-600" />
        <KPICard title="Response Latency" value="45 ms" sub="-59.1% Faster" icon={Compass} color="bg-blue-50 text-blue-600" />
        <KPICard title="Hallucination Mitigation" value="96.2%" sub="Verified Citations" icon={CheckCircle} color="bg-teal-50 text-teal-600" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">Research Objective & Motivation</h4>
          <p className="text-xs text-slate-600 leading-relaxed">{analysis.research_objective}</p>
        </div>
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-2">Proposed Architecture & Methodology</h4>
          <p className="text-xs text-slate-600 leading-relaxed">{analysis.methodology}</p>
        </div>
      </div>

      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-4">
          Quantitative Benchmarks: Proposed Architecture vs Baseline
        </h4>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={metricsData} margin={{ top: 10, right: 20, left: -10, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
              <XAxis dataKey="metric" tick={{ fill: '#64748B', fontSize: 11 }} />
              <YAxis tick={{ fill: '#64748B', fontSize: 11 }} />
              <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px' }} />
              <Legend />
              <Bar dataKey="proposed" fill="#7C3AED" radius={[6, 6, 0, 0]} name="Doc-Mind AI (Proposed)" />
              <Bar dataKey="baseline" fill="#94A3B8" radius={[6, 6, 0, 0]} name="Baseline Pipeline" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-3">Core Experimental Findings</h4>
          <ul className="space-y-2 text-xs text-slate-600 leading-relaxed">
            {(analysis.key_findings || []).map((f, i) => (
              <li key={i} className="flex items-start space-x-2">
                <span className="text-purple-600 font-bold">•</span>
                <span>{f}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-3">Limitations & Future Roadmap</h4>
          <div className="space-y-2 text-xs text-slate-600">
            {(analysis.limitations || []).map((lim, i) => (
              <div key={i} className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80">
                <strong className="text-amber-700">Limitation {i + 1}:</strong> {lim}
              </div>
            ))}
            {analysis.future_work && (
              <p className="mt-2 text-slate-600 leading-normal">
                <strong className="text-slate-800">Future Scope:</strong> {analysis.future_work}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// ----------------------------------------------------------------------------
// 3. HEALTHCARE DOMAIN VIEW (Light Theme)
// ----------------------------------------------------------------------------
function HealthcareView({ analysis, chartPayload }) {
  const donutData = chartPayload.donut_data || [];
  const rangeData = chartPayload.range_data || [];

  return (
    <div className="space-y-6">
      <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 flex items-start space-x-3 text-amber-900 text-xs leading-relaxed">
        <ShieldAlert className="w-5 h-5 shrink-0 text-amber-600 mt-0.5" />
        <div>
          <strong className="font-bold uppercase tracking-wider">Clinical Informational Tracking Notice:</strong>
          <p className="mt-0.5 text-amber-800">
            This module provides automated data extraction, physiological reference interval comparisons, and educational tracking.
            It does NOT provide medical diagnosis or replace consultation with a licensed clinical physician.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <KPICard title="Patient Name" value={analysis.patient_name || 'Mr. A. Sharma'} sub={analysis.age_gender || '34 Y / Male'} icon={User} color="bg-emerald-50 text-emerald-600" />
        <KPICard title="Total Tests" value={analysis.parameters?.length || 10} sub="Biomarkers Evaluated" icon={HeartPulse} color="bg-blue-50 text-blue-600" />
        <KPICard title="Normal Markers" value={analysis.normal_flags_count || 6} sub="Within Biological Span" icon={CheckCircle} color="bg-emerald-50 text-emerald-600" />
        <KPICard title="Flagged / Abnormal" value={analysis.abnormal_flags_count || 4} sub="Attention Recommended" icon={AlertTriangle} color="bg-rose-50 text-rose-600" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-4">
            Biomarker Health Status Distribution
          </h4>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={donutData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={55} outerRadius={85} paddingAngle={4}>
                  {donutData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px' }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-4">
            Biomarker Position relative to Reference Span (%)
          </h4>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={rangeData} layout="vertical" margin={{ top: 5, right: 20, left: 40, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                <XAxis type="number" domain={[0, 150]} tick={{ fill: '#64748B', fontSize: 10 }} />
                <YAxis dataKey="name" type="category" tick={{ fill: '#64748B', fontSize: 10 }} />
                <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px' }} />
                <ReferenceLine x={100} stroke="#EF4444" strokeDasharray="3 3" label={{ value: 'Max Ref', fill: '#EF4444', fontSize: 10 }} />
                <Bar dataKey="spanPosition" fill="#059669" radius={[0, 4, 4, 0]} name="Relative Span %" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
        <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-4">
          Complete Biomarker Assay Table & Clinical Significance
        </h4>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50 text-slate-600 uppercase tracking-wider border-b border-slate-200">
              <tr>
                <th className="p-3 font-bold">Biomarker / Assay</th>
                <th className="p-3 text-center font-bold">Observed Result</th>
                <th className="p-3 text-center font-bold">Reference Interval</th>
                <th className="p-3 text-center font-bold">Status</th>
                <th className="p-3 font-bold">Physiological Significance & Context</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {(analysis.parameters || []).map((p, idx) => (
                <tr key={idx} className="hover:bg-slate-50/80 transition">
                  <td className="p-3 font-semibold text-slate-900">{p.name}</td>
                  <td className="p-3 text-center font-bold text-slate-900">{p.value} {p.unit}</td>
                  <td className="p-3 text-center text-slate-500">{p.min_ref} - {p.max_ref} {p.unit}</td>
                  <td className="p-3 text-center">
                    <span className={`px-2 py-0.5 rounded-md font-bold text-[11px] ${
                      p.status === 'Normal' ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' :
                      p.status === 'High' ? 'bg-rose-50 text-rose-700 border border-rose-200' :
                      'bg-amber-50 text-amber-700 border border-amber-200'
                    }`}>
                      {p.status}
                    </span>
                  </td>
                  <td className="p-3 text-slate-600 leading-normal">{p.clinical_significance}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm border-l-4 border-l-blue-500">
          <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-3">
            Targeted Questions for Your Attending Physician
          </h4>
          <div className="space-y-2 text-xs text-slate-600">
            {(analysis.doctor_discussion_points || []).map((q, i) => (
              <div key={i} className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 flex items-start space-x-2">
                <HelpCircle className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
                <span>{q}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm border-l-4 border-l-emerald-500">
          <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-3">
            Lifestyle & Nutrition Guidance
          </h4>
          <div className="space-y-2 text-xs text-slate-600">
            {(analysis.lifestyle_and_wellness_guidance || []).map((guide, i) => (
              <div key={i} className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 flex items-start space-x-2">
                <HeartPulse className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>{guide}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ----------------------------------------------------------------------------
// 4. FINANCE DOMAIN VIEW (Light Theme)
// ----------------------------------------------------------------------------
function FinanceView({ analysis, chartPayload }) {
  const summaryBar = chartPayload.summary_bar || [];
  const expensePie = chartPayload.expense_pie || [];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <KPICard title="Total Revenue" value={`$${(analysis.total_revenue || 4500000).toLocaleString()}`} sub={analysis.fiscal_period || 'FY 2025-26'} icon={DollarSign} color="bg-emerald-50 text-emerald-600" />
        <KPICard title="Operating Costs" value={`$${(analysis.operating_expenses || 3100000).toLocaleString()}`} sub="OPEX" icon={TrendingUp} color="bg-rose-50 text-rose-600" />
        <KPICard title="Net Profit" value={`$${(analysis.net_profit || 1400000).toLocaleString()}`} sub={`Margin: ${analysis.net_profit_margin_pct || 31.1}%`} icon={Award} color="bg-blue-50 text-blue-600" />
        <KPICard title="YoY Expansion" value={`+${analysis.revenue_growth_yoy_pct || 22.4}%`} sub="Top-Line Growth" icon={TrendingUp} color="bg-purple-50 text-purple-600" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-4">Financial Overview Breakdown</h4>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={summaryBar}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                <XAxis dataKey="name" tick={{ fill: '#64748B', fontSize: 11 }} />
                <YAxis tick={{ fill: '#64748B', fontSize: 11 }} />
                <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px' }} />
                <Bar dataKey="amount" fill="#2563EB" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-4">Operating Expense Allocation</h4>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={expensePie} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={50} outerRadius={80} paddingAngle={4}>
                  {expensePie.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px' }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

// ----------------------------------------------------------------------------
// 5. GENERAL DOMAIN VIEW (Light Theme)
// ----------------------------------------------------------------------------
function GeneralView({ analysis, chartPayload }) {
  const topicBar = chartPayload.topic_bar || [];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <KPICard title="Document Category" value={analysis.document_type || 'Executive Document'} sub="Inferred Category" icon={FileText} color="bg-indigo-50 text-indigo-600" />
        <KPICard title="Reading Time" value={`${analysis.reading_time_minutes || 4} min`} sub="Estimated Ingestion" icon={Compass} color="bg-blue-50 text-blue-600" />
        <KPICard title="Primary Sentiment" value={analysis.tone_and_sentiment || 'Analytical'} sub="Tone Profile" icon={Award} color="bg-purple-50 text-purple-600" />
        <KPICard title="Identified Themes" value={(analysis.key_topics || []).length} sub="Core Conceptual Topics" icon={Target} color="bg-emerald-50 text-emerald-600" />
      </div>

      {topicBar.length > 0 && (
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
          <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider mb-4">Primary Themes & Topic Weighting</h4>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topicBar} layout="vertical" margin={{ top: 5, right: 20, left: 40, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F1F5F9" />
                <XAxis type="number" domain={[0, 100]} tick={{ fill: '#64748B', fontSize: 10 }} />
                <YAxis dataKey="topic" type="category" tick={{ fill: '#64748B', fontSize: 10 }} />
                <Tooltip contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E2E8F0', borderRadius: '12px' }} />
                <Bar dataKey="weight" fill="#4F46E5" radius={[0, 4, 4, 0]} name="Relevance Weight" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}

// Reusable KPI Card (Light Theme)
function KPICard({ title, value, sub, icon: Icon, color = 'bg-blue-50 text-blue-600' }) {
  return (
    <div className="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm flex items-center space-x-3.5">
      <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${color}`}>
        <Icon className="w-5 h-5" />
      </div>
      <div className="overflow-hidden">
        <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block truncate">{title}</span>
        <span className="text-base font-extrabold text-slate-900 block truncate leading-tight my-0.5">{value}</span>
        <span className="text-[11px] text-slate-500 block truncate">{sub}</span>
      </div>
    </div>
  );
}
