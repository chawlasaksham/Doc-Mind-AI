"""
Automated Smoke Test Suite for Doc-Mind AI
"""
from pathlib import Path
import sys

# Add project root to sys.path
PROJECT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_DIR))


from modules.pdf_processor import PDFProcessor
from modules.domain_classifier import DomainClassifier
from modules.rag_engine import RAGEngine
from modules.domain_analyzers import (
    analyze_education,
    analyze_research,
    analyze_healthcare,
    analyze_finance,
    analyze_general,
)
from modules.excel_analyzer import ExcelAnalyzer

def test_pipeline():
    print("🚀 Running Doc-Mind AI Automated Smoke Tests...\n")
    samples_dir = PROJECT_DIR / "samples"

    # Test 1: Marksheet PDF & Education Analyzer
    marksheet_pdf = samples_dir / "sample_marksheet_education.pdf"
    assert marksheet_pdf.exists(), "Marksheet PDF does not exist!"
    proc = PDFProcessor()
    doc_edu = proc.process_pdf(str(marksheet_pdf), filename=marksheet_pdf.name)
    assert doc_edu["total_pages"] >= 1, "Failed to read marksheet pages"
    assert doc_edu["total_words"] > 50, "Extracted too few words from marksheet"
    print(f"✅ PDFProcessor: Processed marksheet ({doc_edu['total_pages']} pages, {doc_edu['total_words']} words, {len(doc_edu['chunks'])} chunks)")

    classifier = DomainClassifier(None)
    cls_edu = classifier.classify_document(doc_edu["full_text"], filename=marksheet_pdf.name)
    assert cls_edu["domain"] == "Education", f"Expected Education domain, got {cls_edu['domain']}"
    print(f"✅ DomainClassifier: Correctly classified marksheet as '{cls_edu['domain']}' (Confidence: {cls_edu['confidence']})")

    edu_data = analyze_education(doc_edu["full_text"], None)
    assert "chart_payload" in edu_data and "bar_data" in edu_data["chart_payload"], "Missing education bar data"
    assert "detailed_summary" in edu_data and len(edu_data["detailed_summary"]) > 100, "Detailed summary missing or too short"
    print("✅ EducationAnalyzer: Successfully generated deep academic summary and Recharts data")

    # Test 2: Research Paper PDF
    res_pdf = samples_dir / "sample_research_paper.pdf"
    doc_res = proc.process_pdf(str(res_pdf), filename=res_pdf.name)
    cls_res = classifier.classify_document(doc_res["full_text"], filename=res_pdf.name)
    assert cls_res["domain"] == "Research", f"Expected Research domain, got {cls_res['domain']}"
    res_data = analyze_research(doc_res["full_text"], None)
    assert "chart_payload" in res_data and "metrics_data" in res_data["chart_payload"], "Missing research metrics data"
    assert "detailed_summary" in res_data and len(res_data["detailed_summary"]) > 100, "Detailed research summary missing"
    print(f"✅ ResearchAnalyzer: Correctly classified research paper as '{cls_res['domain']}' with deep summary & Recharts data")

    # Test 3: Healthcare Lab Report PDF
    health_pdf = samples_dir / "sample_healthcare_report.pdf"
    doc_health = proc.process_pdf(str(health_pdf), filename=health_pdf.name)
    cls_health = classifier.classify_document(doc_health["full_text"], filename=health_pdf.name)
    assert cls_health["domain"] == "Healthcare", f"Expected Healthcare domain, got {cls_health['domain']}"
    health_data = analyze_healthcare(doc_health["full_text"], None)
    assert "chart_payload" in health_data and "donut_data" in health_data["chart_payload"], "Missing healthcare donut data"
    assert "detailed_summary" in health_data and len(health_data["detailed_summary"]) > 100, "Detailed clinical summary missing"
    print(f"✅ HealthcareAnalyzer: Correctly classified lab report as '{cls_health['domain']}' with deep clinical review & Recharts data")

    # Test 4: RAG Engine
    rag = RAGEngine(doc_edu["chunks"])
    results = rag.retrieve("What are the marks in Operating Systems?", top_k=2)
    assert len(results) > 0, "RAG retrieval returned no results"
    print(f"✅ RAGEngine: Successfully retrieved {len(results)} context chunks (Top score: {results[0]['similarity_score']})")

    # Test 5: Excel & CSV Analytics Engine
    sales_csv = samples_dir / "sample_business_sales_analytics.csv"
    analyzer = ExcelAnalyzer(None)
    df, sheets = analyzer.load_dataset(str(sales_csv), filename=sales_csv.name)
    assert len(df) == 120, f"Expected 120 rows, got {len(df)}"
    profile = analyzer.profile_dataframe(df)
    assert profile["total_rows"] == 120
    assert len(profile["numeric_cols"]) >= 4
    charts = analyzer.generate_chart_payload(df, profile)
    assert "distribution" in charts or "categorical" in charts
    ai_story = analyzer.generate_ai_insights(df, profile)
    assert "executive_summary" in ai_story and len(ai_story["executive_summary"]) > 100
    print(f"✅ ExcelAnalyzer: Successfully profiled {profile['total_rows']} rows, generated Recharts payload & deep AI narrative")


    print("\n🎉 ALL TESTS PASSED SUCCESSFULLY! Doc-Mind AI is robust and fully functional.\n")

if __name__ == "__main__":
    test_pipeline()
