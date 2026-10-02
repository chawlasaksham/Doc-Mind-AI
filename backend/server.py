"""
Doc-Mind AI High-Performance FastAPI Server
Provides REST API endpoints for PDF multi-domain intelligence, grounded RAG chatbot,
Excel/CSV automated analytics, and static mounting for the modern React frontend.
"""
import os
import io
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import pandas as pd

# Add parent directory to sys.path
BASE_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(BASE_DIR))

from config import DEFAULT_GEMINI_MODEL, SAMPLES_DIR, SUPPORTED_DOMAINS
from modules.gemini_client import GeminiClient
from modules.pdf_processor import PDFProcessor
from modules.rag_engine import RAGEngine
from modules.domain_classifier import DomainClassifier
from modules.domain_analyzers import (
    analyze_education,
    analyze_research,
    analyze_healthcare,
    analyze_finance,
    analyze_general,
)
from modules.excel_analyzer import ExcelAnalyzer

app = FastAPI(title="Doc-Mind AI Server", version="2.0.0")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
STATE = {
    "api_key": os.getenv("GEMINI_API_KEY", "").strip(),
    "model_name": DEFAULT_GEMINI_MODEL,
    "gemini_client": GeminiClient(api_key=os.getenv("GEMINI_API_KEY", "").strip()),
    "active_pdf": None,
    "pdf_processor": PDFProcessor(),
    "rag_engine": None,
    "active_df": None,
    "active_excel_profile": None,
    "excel_analyzer": None,
}
STATE["excel_analyzer"] = ExcelAnalyzer(STATE["gemini_client"])


# Request Models
class ApiKeyRequest(BaseModel):
    api_key: str
    model_name: Optional[str] = None


class ChatRequest(BaseModel):
    query: str
    chat_history: Optional[List[Dict[str, Any]]] = []



class SheetSelectRequest(BaseModel):
    sheet_name: str


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "app": "Doc-Mind AI",
        "version": "2.0.0",
        "api_key_configured": STATE["gemini_client"].is_configured,
        "model": STATE["model_name"],
    }


@app.get("/api/config")
def get_config():
    return {
        "api_key_configured": STATE["gemini_client"].is_configured,
        "model_name": STATE["model_name"],
        "supported_domains": SUPPORTED_DOMAINS,
    }


@app.post("/api/config/api-key")
def set_api_key(req: ApiKeyRequest):
    key = req.api_key.strip()
    target_model = req.model_name or STATE["model_name"]

    # Test key with a provisional client
    test_client = GeminiClient(api_key=key, model_name=target_model)
    conn = test_client.test_connection()

    if conn["success"]:
        active_model = conn.get("model", target_model)
        STATE["model_name"] = active_model
        STATE["api_key"] = key
        test_client.model_name = active_model
        STATE["gemini_client"] = test_client
        STATE["excel_analyzer"] = ExcelAnalyzer(test_client)
        print(f"✅ Gemini API key activated successfully with model '{active_model}'.")
    else:
        print(f"⚠️ Gemini API key rejected: {conn.get('error')}")

    return {
        "success": conn["success"],
        "model": conn.get("model", target_model),
        "error": conn.get("error", None),
    }


def _process_and_analyze_pdf(file_bytes: bytes, filename: str, override_domain: Optional[str] = None) -> Dict[str, Any]:
    proc = STATE["pdf_processor"]
    doc_data = proc.process_pdf(file_bytes, filename=filename)

    STATE["active_pdf"] = doc_data
    rag = RAGEngine(doc_data["chunks"])
    STATE["rag_engine"] = rag

    classifier = DomainClassifier(STATE["gemini_client"])
    classification = classifier.classify_document(doc_data["full_text"], filename=filename)

    detected_domain = override_domain or classification.get("domain", "General / Business")

    # Run domain specific deep analyzer
    if detected_domain == "Education":
        analysis = analyze_education(doc_data["full_text"], STATE["gemini_client"])
    elif detected_domain == "Research":
        analysis = analyze_research(doc_data["full_text"], STATE["gemini_client"])
    elif detected_domain == "Healthcare":
        analysis = analyze_healthcare(doc_data["full_text"], STATE["gemini_client"])
    elif detected_domain == "Finance":
        analysis = analyze_finance(doc_data["full_text"], STATE["gemini_client"])
    else:
        analysis = analyze_general(doc_data["full_text"], STATE["gemini_client"])

    return {
        "filename": filename,
        "total_pages": doc_data["total_pages"],
        "total_words": doc_data["total_words"],
        "total_chars": doc_data["total_chars"],
        "chunks_count": len(doc_data["chunks"]),
        "domain": detected_domain,
        "confidence": classification.get("confidence", 0.95),
        "sub_category": classification.get("sub_category", f"{detected_domain} Document"),
        "rationale": classification.get("rationale", "Domain pattern identification"),
        "analysis": analysis,
    }


@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), override_domain: Optional[str] = Form(None)):
    try:
        content = await file.read()
        return _process_and_analyze_pdf(content, file.filename, override_domain=override_domain)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/pdf-chat")
def pdf_chat(req: ChatRequest):
    if not STATE.get("rag_engine"):
        raise HTTPException(status_code=400, detail="No active document. Please upload a PDF first.")

    res = STATE["rag_engine"].query_with_llm(
        query=req.query,
        gemini_client=STATE["gemini_client"],
        top_k=4,
        chat_history=req.chat_history,
    )
    return res


def _process_excel_bytes(file_bytes: bytes, filename: str, sheet_name: Optional[str] = None) -> Dict[str, Any]:
    analyzer = STATE["excel_analyzer"]
    df, sheets = analyzer.load_dataset(file_bytes, filename=filename, sheet_name=sheet_name)
    STATE["active_df"] = df

    profile = analyzer.profile_dataframe(df)
    STATE["active_excel_profile"] = profile

    chart_payload = analyzer.generate_chart_payload(df, profile)
    ai_story = analyzer.generate_ai_insights(df, profile)

    preview_rows = df.head(30).fillna("").to_dict(orient="records")

    return {
        "filename": filename,
        "sheets": sheets,
        "active_sheet": sheet_name or (sheets[0] if sheets else "Default"),
        "profile": profile,
        "chart_payload": chart_payload,
        "ai_story": ai_story,
        "preview_rows": preview_rows,
    }


@app.post("/api/upload-excel")
async def upload_excel(file: UploadFile = File(...), sheet_name: Optional[str] = Form(None)):
    try:
        content = await file.read()
        return _process_excel_bytes(content, file.filename, sheet_name=sheet_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/excel-chat")
def excel_chat(req: ChatRequest):
    df = STATE.get("active_df")
    profile = STATE.get("active_excel_profile")
    if df is None or profile is None:
        raise HTTPException(status_code=400, detail="No active spreadsheet. Please upload an Excel/CSV file first.")

    answer = STATE["excel_analyzer"].answer_data_query(
        query=req.query,
        df=df,
        profile=profile,
        chat_history=req.chat_history,
    )
    return {"answer": answer}


@app.get("/api/load-sample/{sample_id}")
def load_sample(sample_id: str):
    """Instant 1-click loading for pre-generated sample benchmarks."""
    samples_dir = BASE_DIR / "samples"
    if sample_id == "marksheet":
        path = samples_dir / "sample_marksheet_education.pdf"
        data = open(path, "rb").read()
        return _process_and_analyze_pdf(data, path.name)
    elif sample_id == "research":
        path = samples_dir / "sample_research_paper.pdf"
        data = open(path, "rb").read()
        return _process_and_analyze_pdf(data, path.name)
    elif sample_id == "healthcare":
        path = samples_dir / "sample_healthcare_report.pdf"
        data = open(path, "rb").read()
        return _process_and_analyze_pdf(data, path.name)
    elif sample_id == "sales":
        path = samples_dir / "sample_business_sales_analytics.csv"
        data = open(path, "rb").read()
        return _process_excel_bytes(data, path.name)
    else:
        raise HTTPException(status_code=404, detail="Sample not found")


# Static Frontend Mounting
dist_path = BASE_DIR / "frontend" / "dist"
if dist_path.exists():
    app.mount("/", StaticFiles(directory=str(dist_path), html=True), name="static")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"⚡ Starting Doc-Mind AI Server on http://localhost:{port}")
    uvicorn.run("backend.server:app", host="0.0.0.0", port=port, reload=True)
