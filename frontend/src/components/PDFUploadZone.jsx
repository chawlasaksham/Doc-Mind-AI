import React, { useRef } from 'react';
import { UploadCloud, FileText, CheckCircle2, Loader2 } from 'lucide-react';

export default function PDFUploadZone({ onFileUpload, isProcessing, activeDoc }) {
  const fileInputRef = useRef(null);

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.name.endsWith('.pdf')) {
        onFileUpload(file);
      } else {
        alert('Please upload a PDF file.');
      }
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      onFileUpload(e.target.files[0]);
    }
  };

  return (
    <div className="mb-6">
      <div
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-2xl p-7 text-center cursor-pointer transition-all duration-200 ${
          isProcessing
            ? 'border-blue-400 bg-blue-50/50'
            : 'border-slate-300 hover:border-blue-500 bg-white hover:bg-slate-50/80 shadow-xs'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleChange}
          className="hidden"
        />

        <div className="flex flex-col items-center justify-center space-y-2.5">
          <div className="w-12 h-12 rounded-2xl bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600 shadow-sm">
            {isProcessing ? (
              <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
            ) : (
              <UploadCloud className="w-6 h-6" />
            )}
          </div>

          <div>
            <h4 className="text-sm font-bold text-slate-900">
              {isProcessing ? 'AI Agent Analyzing Document & Domain...' : 'Upload PDF Document for Analysis'}
            </h4>
            <p className="text-xs text-slate-500 mt-0.5">
              Drag & drop or click to upload marksheets, research papers, healthcare lab assays, or business reports
            </p>
          </div>

          {activeDoc && !isProcessing && (
            <div className="flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
              <span>Loaded: {activeDoc.filename} ({activeDoc.total_pages} pages, {activeDoc.total_words?.toLocaleString()} words)</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
