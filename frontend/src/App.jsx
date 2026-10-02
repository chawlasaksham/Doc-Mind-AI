import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  GraduationCap,
  Microscope,
  Activity,
  TrendingUp,
  FileSearch,
} from 'lucide-react';
import Sidebar from './components/Sidebar';
import ApiKeyModal from './components/ApiKeyModal';
import PDFUploadZone from './components/PDFUploadZone';
import DomainBadge from './components/DomainBadge';
import DomainDashboard from './components/DomainDashboard';
import ExcelDashboard from './components/ExcelDashboard';
import RightChatbot from './components/RightChatbot';

export default function App() {
  const [activeTab, setActiveTab] = useState('pdf');
  const [isKeyModalOpen, setIsKeyModalOpen] = useState(false);
  const [apiConfig, setApiConfig] = useState({ isConfigured: false, model: 'gemini-2.5-flash' });

  // PDF Intelligence State
  const [activePdfDoc, setActivePdfDoc] = useState(null);
  const [isPdfLoading, setIsPdfLoading] = useState(false);
  const [pdfChatHistory, setPdfChatHistory] = useState([]);
  const [isPdfChatting, setIsPdfChatting] = useState(false);

  // Excel Analytics State
  const [activeExcelData, setActiveExcelData] = useState(null);
  const [isExcelLoading, setIsExcelLoading] = useState(false);
  const [excelChatHistory, setExcelChatHistory] = useState([]);
  const [isExcelChatting, setIsExcelChatting] = useState(false);

  // Fetch initial config on load
  useEffect(() => {
    fetch('/api/config')
      .then((res) => res.json())
      .then((data) => {
        setApiConfig({
          isConfigured: data.api_key_configured,
          model: data.model_name || 'gemini-2.5-flash',
        });
      })
      .catch((err) => console.log('Config fetch offline, operating local mode.'));
  }, []);

  const handleSaveApiKey = async (apiKey, model) => {
    try {
      const res = await fetch('/api/config/api-key', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api_key: apiKey, model_name: model }),
      });
      const data = await res.json();
      if (data.success) {
        setApiConfig({ isConfigured: true, model: data.model });
      }
      return data;
    } catch (err) {
      return { success: false, error: err.message };
    }
  };

  // Upload Custom PDF
  const handleUploadPdf = async (file, overrideDomain = null) => {
    setIsPdfLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    if (overrideDomain) {
      formData.append('override_domain', overrideDomain);
    }

    try {
      const res = await fetch('/api/upload-pdf', {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error('Upload failed');
      const data = await res.json();
      setActivePdfDoc(data);
      setPdfChatHistory([]);
    } catch (err) {
      alert(`PDF Analysis Error: ${err.message}`);
    } finally {
      setIsPdfLoading(false);
    }
  };

  // PDF Grounded Chat Query
  const handlePdfChat = async (query) => {
    if (!activePdfDoc) {
      setPdfChatHistory((prev) => [
        ...prev,
        { role: 'user', content: query },
        { role: 'assistant', content: '⚠️ Please upload a PDF document first before asking questions.' },
      ]);
      return;
    }

    setIsPdfChatting(true);
    const newHistory = [...pdfChatHistory, { role: 'user', content: query }];
    setPdfChatHistory(newHistory);

    try {
      // Strip extraneous fields like retrieved_chunks from history before sending to API
      const sanitizedHistory = newHistory.slice(-6).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const res = await fetch('/api/pdf-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          chat_history: sanitizedHistory,
        }),
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || `Chat request failed with status ${res.status}`);
      }
      const data = await res.json();

      setPdfChatHistory([
        ...newHistory,
        {
          role: 'assistant',
          content: data.answer,
          retrieved_chunks: data.retrieved_chunks,
        },
      ]);
    } catch (err) {
      setPdfChatHistory([
        ...newHistory,
        {
          role: 'assistant',
          content: `⚠️ Could not get answer: ${err.message}`,
        },
      ]);
    } finally {
      setIsPdfChatting(false);
    }
  };

  // Upload Custom Excel
  const handleUploadExcel = async (file, sheetName = null) => {
    setIsExcelLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    if (sheetName) {
      formData.append('sheet_name', sheetName);
    }

    try {
      const res = await fetch('/api/upload-excel', {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error('Spreadsheet processing failed');
      const data = await res.json();
      setActiveExcelData(data);
      setExcelChatHistory([]);
    } catch (err) {
      alert(`Excel Analysis Error: ${err.message}`);
    } finally {
      setIsExcelLoading(false);
    }
  };

  // Excel Conversational Chat
  const handleExcelChat = async (query) => {
    if (!activeExcelData) {
      setExcelChatHistory((prev) => [
        ...prev,
        { role: 'user', content: query },
        { role: 'assistant', content: '⚠️ Please upload an Excel or CSV file first before asking questions.' },
      ]);
      return;
    }

    setIsExcelChatting(true);
    const newHistory = [...excelChatHistory, { role: 'user', content: query }];
    setExcelChatHistory(newHistory);

    try {
      const sanitizedHistory = newHistory.slice(-6).map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const res = await fetch('/api/excel-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          chat_history: sanitizedHistory,
        }),
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || `Data chat request failed with status ${res.status}`);
      }
      const data = await res.json();

      setExcelChatHistory([
        ...newHistory,
        { role: 'assistant', content: data.answer },
      ]);
    } catch (err) {
      setExcelChatHistory([
        ...newHistory,
        { role: 'assistant', content: `⚠️ Error: ${err.message}` },
      ]);
    } finally {
      setIsExcelChatting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex text-slate-900 selection:bg-blue-600 selection:text-white">
      {/* 1. Left Sidebar: Tabs Navigation & Metadata */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        apiConfig={apiConfig}
        onOpenKeyModal={() => setIsKeyModalOpen(true)}
      />

      {/* 2. Center: Main Content & Dynamic Analytics Dashboards */}
      <main className="flex-1 overflow-y-auto px-6 py-6 min-w-0">
        <div className="max-w-5xl mx-auto space-y-6">
          {/* TAB 1: PDF Intelligence */}
          {activeTab === 'pdf' && (
            <div className="space-y-6">
              <PDFUploadZone
                onFileUpload={handleUploadPdf}
                isProcessing={isPdfLoading}
                activeDoc={activePdfDoc}
              />

              {!activePdfDoc && !isPdfLoading && (
                <div className="bg-white rounded-2xl border border-slate-200/80 p-8 shadow-xs text-center space-y-6">
                  <div className="max-w-md mx-auto space-y-2">
                    <div className="w-12 h-12 mx-auto rounded-2xl bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600 shadow-xs">
                      <Sparkles className="w-6 h-6 text-blue-600" />
                    </div>
                    <h3 className="text-base font-bold text-slate-900">
                      Adaptive Multi-Domain Intelligence
                    </h3>
                    <p className="text-xs text-slate-500 leading-relaxed">
                      Upload any PDF document above. The system automatically classifies its domain and synthesizes a tailored analytical dashboard with grounded RAG chatbot assistance.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5 text-left pt-2">
                    <div className="p-3.5 rounded-xl bg-slate-50/70 border border-slate-200/60 space-y-1.5">
                      <div className="flex items-center space-x-2 text-blue-700 font-bold text-xs">
                        <GraduationCap className="w-4 h-4" />
                        <span>Education</span>
                      </div>
                      <p className="text-[11px] text-slate-500 leading-snug">
                        Academic score distributions, performance radar charts, GPA & subject analysis.
                      </p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-50/70 border border-slate-200/60 space-y-1.5">
                      <div className="flex items-center space-x-2 text-purple-700 font-bold text-xs">
                        <Microscope className="w-4 h-4" />
                        <span>Research</span>
                      </div>
                      <p className="text-[11px] text-slate-500 leading-snug">
                        Methodology analysis, baseline benchmarking, and scientific citation metrics.
                      </p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-50/70 border border-slate-200/60 space-y-1.5">
                      <div className="flex items-center space-x-2 text-rose-700 font-bold text-xs">
                        <Activity className="w-4 h-4" />
                        <span>Healthcare</span>
                      </div>
                      <p className="text-[11px] text-slate-500 leading-snug">
                        Diagnostic report breakdown, abnormal biomarker flags, and clinical context.
                      </p>
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-50/70 border border-slate-200/60 space-y-1.5">
                      <div className="flex items-center space-x-2 text-emerald-700 font-bold text-xs">
                        <TrendingUp className="w-4 h-4" />
                        <span>Finance</span>
                      </div>
                      <p className="text-[11px] text-slate-500 leading-snug">
                        Revenue & expense breakdowns, operating margins, and risk factor audits.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {activePdfDoc && (
                <>
                  <DomainBadge
                    domain={activePdfDoc.domain}
                    confidence={activePdfDoc.confidence}
                    subCategory={activePdfDoc.sub_category}
                    rationale={activePdfDoc.rationale}
                    onOverrideDomain={(newDom) => handleUploadPdf(new File([new Blob()], activePdfDoc.filename), newDom)}
                  />

                  <DomainDashboard
                    domain={activePdfDoc.domain}
                    analysis={activePdfDoc.analysis}
                  />
                </>
              )}
            </div>
          )}

          {/* TAB 2: Excel & CSV Analytics */}
          {activeTab === 'excel' && (
            <ExcelDashboard
              excelData={activeExcelData}
              onFileUpload={handleUploadExcel}
              isUploading={isExcelLoading}
              onSheetChange={(sheet) => handleUploadExcel(new File([new Blob()], activeExcelData.filename), sheet)}
            />
          )}
        </div>
      </main>

      {/* 3. Right: Dedicated Chatbot Panel */}
      <RightChatbot
        activeTab={activeTab}
        pdfChatHistory={pdfChatHistory}
        onSendPdfQuery={handlePdfChat}
        isPdfChatting={isPdfChatting}
        domain={activePdfDoc?.domain}
        excelChatHistory={excelChatHistory}
        onSendExcelQuery={handleExcelChat}
        isExcelChatting={isExcelChatting}
        aiStory={activeExcelData?.ai_story}
        onClearChat={() => {
          if (activeTab === 'pdf') setPdfChatHistory([]);
          else setExcelChatHistory([]);
        }}
      />

      {/* Gemini API Key Modal */}
      <ApiKeyModal
        isOpen={isKeyModalOpen}
        onClose={() => setIsKeyModalOpen(false)}
        apiConfig={apiConfig}
        onSaveKey={handleSaveApiKey}
      />
    </div>
  );
}
