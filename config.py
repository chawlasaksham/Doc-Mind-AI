"""
Doc-Mind AI Configuration Settings
"""
import os
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# Base paths
PROJECT_ROOT = Path(__file__).parent.resolve()
SAMPLES_DIR = PROJECT_ROOT / "samples"
SAMPLES_DIR.mkdir(exist_ok=True)

# Default Gemini Model
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
FALLBACK_GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-pro"]

# Supported Domains
SUPPORTED_DOMAINS = [
    "Education",
    "Research",
    "Healthcare",
    "Finance",
    "General / Business",
]

# Domain Icons and Accent Colors
DOMAIN_METADATA = {
    "Education": {
        "icon": "🎓",
        "color": "#3B82F6",  # Blue
        "description": "Academic records, Marksheets, Transcripts & Performance reports"
    },
    "Research": {
        "icon": "🔬",
        "color": "#8B5CF6",  # Purple
        "description": "Scientific papers, Technical studies & Literature reviews"
    },
    "Healthcare": {
        "icon": "🩺",
        "color": "#10B981",  # Emerald Green
        "description": "Diagnostic reports, Lab tests, Vitals & Health assessments"
    },
    "Finance": {
        "icon": "💼",
        "color": "#F59E0B",  # Amber/Gold
        "description": "Financial statements, Revenue & Expense reports, Balance sheets"
    },
    "General / Business": {
        "icon": "📄",
        "color": "#6366F1",  # Indigo
        "description": "Business documents, Executive summaries, Proposals & Contracts"
    },
}

# RAG Configuration
RAG_CHUNK_SIZE = 800
RAG_CHUNK_OVERLAP = 150
RAG_TOP_K = 4
