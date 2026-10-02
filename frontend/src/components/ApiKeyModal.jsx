import React, { useState } from 'react';
import { X, Key, CheckCircle, AlertTriangle, Cpu, ExternalLink } from 'lucide-react';

export default function ApiKeyModal({ isOpen, onClose, apiConfig, onSaveKey }) {
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState(apiConfig.model || 'gemini-2.5-flash');
  const [loading, setLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState(null);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!apiKey.trim()) return;

    setLoading(true);
    setStatusMessage(null);

    const result = await onSaveKey(apiKey.trim(), model);
    setLoading(false);

    if (result.success) {
      setStatusMessage({ type: 'success', text: `Connected successfully with ${result.model}!` });
      setTimeout(() => {
        onClose();
      }, 1200);
    } else {
      setStatusMessage({ type: 'error', text: result.error || 'Failed to connect. Please check key validity.' });
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-fade-in">
      <div className="bg-white w-full max-w-md rounded-2xl p-6 border border-slate-200 shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-700 p-1 rounded-lg hover:bg-slate-100 transition"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center space-x-3 mb-5">
          <div className="w-10 h-10 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600">
            <Key className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900">Google Gemini API Key</h3>
            <p className="text-xs text-slate-500">Enable advanced contextual reasoning & AI chat</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1.5 uppercase tracking-wider">
              Gemini API Key
            </label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Paste your AIzaSy... key"
              className="w-full bg-slate-50 border border-slate-300 rounded-xl px-4 py-2.5 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition"
              required
            />
            {apiKey.trim() && !apiKey.trim().startsWith('AIzaSy') && (
              <p className="mt-1.5 text-[11px] text-amber-700 bg-amber-50 border border-amber-200 rounded-lg p-2 leading-tight">
                💡 <strong>Notice:</strong> Gemini API keys from Google AI Studio begin with <code className="bg-amber-100 px-1 rounded font-mono">AIzaSy...</code>. If your key begins with another prefix (like <code className="bg-amber-100 px-1 rounded font-mono">AQ.</code>), ensure you are copying the API key from the link below.
              </p>
            )}
            <p className="mt-1.5 text-[11px] text-slate-500 flex items-center justify-between">
              <span>Saved locally for this session</span>
              <a
                href="https://aistudio.google.com/app/apikey"
                target="_blank"
                rel="noreferrer"
                className="text-blue-600 hover:underline flex items-center space-x-1 font-semibold"
              >
                <span>Get API key from Google AI Studio</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </p>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1.5 uppercase tracking-wider">
              Active Gemini Model
            </label>
            <div className="relative">
              <select
                value={model}
                onChange={(e) => setModel(e.target.value)}
                className="w-full bg-slate-50 border border-slate-300 rounded-xl px-4 py-2.5 text-xs font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none cursor-pointer"
              >
                <option value="gemini-2.5-flash">gemini-2.5-flash (Google Recommended & Fast)</option>
                <option value="gemini-2.0-flash">gemini-2.0-flash (Flash 2.0)</option>
                <option value="gemini-1.5-flash">gemini-1.5-flash (Legacy)</option>
                <option value="gemini-2.5-pro">gemini-2.5-pro (Deep Reasoning)</option>
              </select>
              <Cpu className="w-4 h-4 text-slate-400 absolute right-3.5 top-3 pointer-events-none" />
            </div>
          </div>

          {statusMessage && (
            <div
              className={`p-3 rounded-xl text-xs flex items-center space-x-2 font-medium ${
                statusMessage.type === 'success'
                  ? 'bg-emerald-50 border border-emerald-200 text-emerald-800'
                  : 'bg-rose-50 border border-rose-200 text-rose-800'
              }`}
            >
              {statusMessage.type === 'success' ? (
                <CheckCircle className="w-4 h-4 shrink-0 text-emerald-600" />
              ) : (
                <AlertTriangle className="w-4 h-4 shrink-0 text-rose-600" />
              )}
              <span className="leading-snug">{statusMessage.text}</span>
            </div>
          )}

          <div className="pt-2 flex items-center justify-end space-x-2.5">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-900 rounded-xl hover:bg-slate-100 transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2.5 rounded-xl text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 transition shadow-sm"
            >
              {loading ? 'Verifying...' : 'Save & Connect'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
