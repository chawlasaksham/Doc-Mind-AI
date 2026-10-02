"""
Domain Analyzers Package for Doc-Mind AI
"""
from .education import analyze_education
from .research import analyze_research
from .healthcare import analyze_healthcare
from .finance import analyze_finance
from .general import analyze_general

__all__ = [
    "analyze_education",
    "analyze_research",
    "analyze_healthcare",
    "analyze_finance",
    "analyze_general",
]
