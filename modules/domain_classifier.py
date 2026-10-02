"""
Agentic Domain Classifier for Doc-Mind AI
Analyzes document text and automatically identifies the domain:
Education, Research, Healthcare, Finance, or General/Business.
"""
from typing import Dict, Any, Optional
import re
from config import SUPPORTED_DOMAINS


class DomainClassifier:
    def __init__(self, gemini_client=None):
        self.client = gemini_client

    def classify_document(self, text_sample: str, filename: str = "") -> Dict[str, Any]:
        """
        Classifies the document into one of the supported domains.
        Uses Gemini LLM if configured; otherwise uses robust heuristic rules.
        """
        if self.client and self.client.is_configured:
            try:
                return self._classify_with_gemini(text_sample, filename)
            except Exception as e:
                print(f"Gemini classification fallback triggered: {e}")
                return self._classify_heuristically(text_sample, filename)
        else:
            return self._classify_heuristically(text_sample, filename)

    def _classify_with_gemini(self, text: str, filename: str) -> Dict[str, Any]:
        # Truncate text sample to first ~2500 words
        sample = " ".join(text.split()[:2500])

        system_instruction = (
            "You are the central Domain Identification Agent of Doc-Mind AI. "
            "Your role is to inspect the uploaded document title, structure, and text, "
            "and assign it to the most specific domain among: "
            "['Education', 'Research', 'Healthcare', 'Finance', 'General / Business']. "
            "Always respond strictly with a valid JSON object."
        )

        prompt = f"""
Analyze this document and determine its domain.

FILENAME: {filename}
DOCUMENT CONTENT PREVIEW:
{sample}

Respond in this exact JSON structure:
{{
  "domain": "One of: Education, Research, Healthcare, Finance, General / Business",
  "confidence": 0.95,
  "rationale": "Detailed explanation of why this document matches the chosen domain",
  "sub_category": "e.g., University Marksheet / Clinical Lab Report / IEEE Research Paper / Quarterly P&L",
  "detected_signals": ["Key signal 1", "Key signal 2", "Key signal 3"],
  "recommended_widgets": ["metric_cards", "chart_type", "summary_block"]
}}
"""
        result = self.client.generate_json(prompt, system_instruction=system_instruction)

        # Validate domain output
        domain = result.get("domain", "General / Business").strip()
        matched = False
        for valid in SUPPORTED_DOMAINS:
            if valid.lower() in domain.lower():
                result["domain"] = valid
                matched = True
                break
        if not matched:
            result["domain"] = "General / Business"

        return result

    def _classify_heuristically(self, text: str, filename: str) -> Dict[str, Any]:
        """Fast fallback rule-based classifier based on domain keywords and structural tokens."""
        lower_text = (filename + " " + text[:6000]).lower()

        scores = {
            "Education": 0,
            "Research": 0,
            "Healthcare": 0,
            "Finance": 0,
            "General / Business": 1,  # Baseline
        }

        # Education signals
        edu_keywords = [
            "marksheet", "grade sheet", "transcript", "cgpa", "sgpa", "gpa", "credits",
            "roll no", "enrollment", "examination", "semester", "course code", "marks obtained",
            "max marks", "percentage", "internal marks", "university", "institute of information technology",
            "b.tech", "m.tech", "bachelor", "master", "curriculum", "subject", "student"
        ]
        for kw in edu_keywords:
            if kw in lower_text:
                scores["Education"] += 2

        # Research signals
        research_keywords = [
            "abstract", "methodology", "proposed architecture", "literature review",
            "dataset", "experimental results", "conclusion", "future work", "references",
            "ieee", "arxiv", "acm", "citation", "ablation study", "baseline", "deep learning",
            "machine learning", "neural network", "state of the art", "sota"
        ]
        for kw in research_keywords:
            if kw in lower_text:
                scores["Research"] += 2

        # Healthcare signals
        health_keywords = [
            "patient", "lab report", "diagnostic", "blood test", "hemoglobin", "platelet",
            "rbc", "wbc", "cholesterol", "triglycerides", "glucose", "hba1c", "specimen",
            "reference range", "normal range", "doctor", "physician", "pathology", "clinic",
            "hospital", "mg/dl", "u/l", "serum", "biomarker", "vital signs"
        ]
        for kw in health_keywords:
            if kw in lower_text:
                scores["Healthcare"] += 2

        # Finance signals
        finance_keywords = [
            "revenue", "expenses", "net profit", "ebitda", "balance sheet", "income statement",
            "cash flow", "assets", "liabilities", "fiscal year", "q1", "q2", "q3", "q4",
            "shareholder", "equity", "dividend", "operating margin", "capital expenditure",
            "invoice", "financial performance", "roi", "gross margin"
        ]
        for kw in finance_keywords:
            if kw in lower_text:
                scores["Finance"] += 2

        # Find maximum scoring domain
        best_domain = max(scores, key=scores.get)
        max_score = scores[best_domain]
        confidence = min(0.95, max(0.60, max_score / 10.0))

        signals = {
            "Education": ["Academic terms", "Marks / Grading scheme", "Course identifiers"],
            "Research": ["Scientific structure", "Abstract / Methodology", "Citations / Findings"],
            "Healthcare": ["Clinical biomarkers", "Reference ranges", "Diagnostic parameters"],
            "Finance": ["Monetary metrics", "Revenue / Expense indicators", "Fiscal disclosures"],
            "General / Business": ["General narrative text", "Standard business terminology"],
        }

        return {
            "domain": best_domain,
            "confidence": round(confidence, 2),
            "rationale": f"Detected strong keyword presence and document layout corresponding to {best_domain}.",
            "sub_category": f"{best_domain} Document",
            "detected_signals": signals.get(best_domain, ["Document text patterns"]),
            "recommended_widgets": ["metric_cards", "charts", "summary_block"],
        }
