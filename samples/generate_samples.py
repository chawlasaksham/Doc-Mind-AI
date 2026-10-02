"""
Sample Generator for Doc-Mind AI
Creates realistic sample PDFs and CSV files for immediate demonstration of all domains and Excel analytics.
"""
from pathlib import Path
import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

SAMPLES_DIR = Path(__file__).parent.resolve()
SAMPLES_DIR.mkdir(exist_ok=True)


def create_sample_marksheet_pdf():
    pdf_path = SAMPLES_DIR / "sample_marksheet_education.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        alignment=1,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=12
    )
    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#475569'),
        spaceAfter=18
    )
    normal_style = styles['Normal']

    story = []
    story.append(Paragraph("JAYPEE INSTITUTE OF INFORMATION TECHNOLOGY", title_style))
    story.append(Paragraph("OFFICIAL STATEMENT OF GRADES & MARKSHEET — SEMESTER VI", sub_style))

    student_data = [
        [Paragraph("<b>Student Name:</b> Mrigank Rai", normal_style), Paragraph("<b>Enrollment No:</b> 9923103126", normal_style)],
        [Paragraph("<b>Program:</b> B.Tech Computer Science & Engg", normal_style), Paragraph("<b>Academic Year:</b> 2025-2026", normal_style)],
        [Paragraph("<b>Institution Code:</b> JIIT-128", normal_style), Paragraph("<b>Status:</b> Regular", normal_style)],
    ]
    t_student = Table(student_data, colWidths=[260, 260])
    t_student.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_student)
    story.append(Spacer(1, 16))

    story.append(Paragraph("<b>Course-Wise Evaluation Records:</b>", styles['Heading3']))
    courses_data = [
        ["Course Code", "Subject Name", "Credits", "Max Marks", "Marks Obtained", "Grade"],
        ["CS201", "Data Structures & Algorithms", "4", "100", "92", "A+"],
        ["CS204", "Database Management Systems", "4", "100", "95", "A+"],
        ["CS301", "Computer Networks", "3", "100", "84", "A"],
        ["CS302", "Operating Systems", "3", "100", "78", "B+"],
        ["CS405", "Artificial Intelligence & ML", "4", "100", "91", "A+"],
        ["HS102", "Professional Ethics & Communication", "2", "100", "88", "A"],
    ]
    t_courses = Table(courses_data, colWidths=[70, 210, 50, 65, 75, 50])
    t_courses.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (1,1), (1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_courses)
    story.append(Spacer(1, 16))

    summary_data = [
        [Paragraph("<b>Total Maximum Marks:</b> 600", normal_style), Paragraph("<b>Total Marks Obtained:</b> 528", normal_style)],
        [Paragraph("<b>Percentage:</b> 88.0%", normal_style), Paragraph("<b>Semester GPA (SGPA):</b> 9.15 / 10.0", normal_style)],
        [Paragraph("<b>Result:</b> PASSED WITH DISTINCTION", normal_style), Paragraph("<b>Academic Standing:</b> Excellent", normal_style)],
    ]
    t_summary = Table(summary_data, colWidths=[260, 260])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93C5FD')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 14))

    remarks = (
        "<b>Controller of Examination Remarks:</b> Candidate has displayed exemplary competence in core computing "
        "disciplines, especially Databases and Machine Learning. Recommended for advanced honors projects."
    )
    story.append(Paragraph(remarks, normal_style))

    doc.build(story)
    print(f"Created: {pdf_path}")


def create_sample_research_paper_pdf():
    pdf_path = SAMPLES_DIR / "sample_research_paper.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        alignment=1,
        textColor=colors.HexColor('#581C87'),
        spaceAfter=10
    )
    author_style = ParagraphStyle(
        'DocAuth',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#334155'),
        spaceAfter=15
    )
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9.5, leading=13, spaceAfter=8)

    story = []
    story.append(Paragraph("Doc-Mind AI: Multi-Domain Adaptive Document Intelligence using Agentic RAG", title_style))
    story.append(Paragraph("Saksham Chawla, Mrigank Rai, Aditya Kumar Gupta<br/><i>Department of Computer Science & Engineering, Jaypee Institute of Information Technology</i>", author_style))

    story.append(Paragraph("<b>ABSTRACT</b>", styles['Heading3']))
    abstract_text = (
        "Digital document processing systems conventionally employ fixed pipelines and static dashboards that fail "
        "to adapt to heterogeneous domains such as education, healthcare, and finance. In this paper, we introduce "
        "<b>Doc-Mind AI</b>, an agentic multi-domain document intelligence platform. The architecture employs "
        "dynamic domain classification coupled with Retrieval-Augmented Generation (RAG) and automatic UI "
        "widget synthesis. Experimental evaluations demonstrate a 94.6% domain classification accuracy, "
        "a 42% reduction in user query response latency, and substantial improvement in context-grounded hallucination mitigation."
    )
    story.append(Paragraph(abstract_text, body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>1. RESEARCH OBJECTIVE & PROBLEM STATEMENT</b>", styles['Heading3']))
    obj_text = (
        "Existing document workflows suffer from two primary limitations: (1) manual extraction of unstructured data "
        "is labor-intensive and error-prone, and (2) static dashboards cannot adapt their visual structure to heterogeneous "
        "document types. Our objective is to construct an autonomous agentic pipeline where the document determines "
        "the analysis, and the analysis dynamically shapes the visualization dashboard."
    )
    story.append(Paragraph(obj_text, body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>2. SYSTEM ARCHITECTURE & METHODOLOGY</b>", styles['Heading3']))
    meth_text = (
        "The proposed system incorporates a multi-tier agentic architecture: (i) Ingestion and Sliding-Window Chunking, "
        "(ii) LLM-powered Zero-Shot Domain Classification, (iii) In-Memory Vector Similarity RAG Retrieval, and (iv) Dynamic "
        "Widget Synthesis for Plotly visualizations. Large Language Models (Gemini 2.5 Flash) provide reasoning and synthesis."
    )
    story.append(Paragraph(meth_text, body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>3. EXPERIMENTAL RESULTS & BENCHMARKS</b>", styles['Heading3']))
    res_data = [
        ["Evaluation Metric", "Baseline Pipeline", "Doc-Mind AI (Proposed)", "Gain / Improvement"],
        ["Classification Accuracy", "87.2%", "94.6%", "+7.4%"],
        ["Retrieval Precision@5", "82.4%", "93.1%", "+10.7%"],
        ["Response Latency (ms)", "110 ms", "45 ms", "-59.1% (Faster)"],
        ["User Task Completion", "68.0%", "92.7%", "+24.7%"],
    ]
    t_res = Table(res_data, colWidths=[140, 110, 140, 130])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#581C87')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#FAF5FF')]),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_res)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>4. CONCLUSION & FUTURE SCOPE</b>", styles['Heading3']))
    conc_text = (
        "Doc-Mind AI demonstrates that combining Agentic AI with Retrieval-Augmented Generation yields an adaptive, "
        "scalable document platform. Future research will explore multi-modal OCR ingestion for handwritten manuscripts "
        "and collaborative multi-agent cross-document syntheses."
    )
    story.append(Paragraph(conc_text, body_style))

    doc.build(story)
    print(f"Created: {pdf_path}")


def create_sample_healthcare_pdf():
    pdf_path = SAMPLES_DIR / "sample_healthcare_report.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        alignment=1,
        textColor=colors.HexColor('#065F46'),
        spaceAfter=8
    )
    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#047857'),
        spaceAfter=14
    )
    normal_style = styles['Normal']

    story = []
    story.append(Paragraph("METROPOLIS CLINICAL DIAGNOSTIC LABORATORIES", title_style))
    story.append(Paragraph("COMPREHENSIVE BIOCHEMICAL & HEMATOLOGY PROFILE", sub_style))

    patient_data = [
        [Paragraph("<b>Patient Name:</b> Mr. A. Sharma", normal_style), Paragraph("<b>Age / Gender:</b> 34 Y / Male", normal_style)],
        [Paragraph("<b>Referred By:</b> Dr. S. K. Sen, MD", normal_style), Paragraph("<b>Report Date:</b> 18-Sep-2026", normal_style)],
        [Paragraph("<b>Specimen:</b> Serum & Whole Blood EDTA", normal_style), Paragraph("<b>Sample ID:</b> LAB-992014", normal_style)],
    ]
    t_patient = Table(patient_data, colWidths=[260, 260])
    t_patient.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#A7F3D0')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_patient)
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>Biochemical & Hematological Parameters:</b>", styles['Heading3']))
    labs_data = [
        ["Test / Biomarker", "Observed Result", "Units", "Biological Reference Range", "Status"],
        ["Hemoglobin (Hb)", "14.8", "g/dL", "13.0 - 17.5", "Normal"],
        ["Total Leukocyte Count (WBC)", "6800", "/mcL", "4000 - 11000", "Normal"],
        ["Platelet Count", "265", "x10^3/mcL", "150 - 450", "Normal"],
        ["Fasting Blood Sugar (Glucose)", "118", "mg/dL", "70 - 100", "HIGH"],
        ["HbA1c (Glycated Hemoglobin)", "6.1", "%", "4.0 - 5.6", "HIGH"],
        ["Total Cholesterol", "224", "mg/dL", "125 - 200", "HIGH"],
        ["Triglycerides", "165", "mg/dL", "50 - 150", "HIGH"],
        ["HDL Cholesterol (Good)", "51", "mg/dL", "40 - 60", "Normal"],
        ["Serum Creatinine", "0.92", "mg/dL", "0.70 - 1.30", "Normal"],
        ["Vitamin D3 (25-Hydroxy)", "21.5", "ng/mL", "30.0 - 100.0", "LOW"],
    ]
    t_labs = Table(labs_data, colWidths=[170, 85, 75, 130, 60])
    t_labs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#065F46')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (0,1), (0,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_labs)
    story.append(Spacer(1, 14))

    disclaimer = (
        "<b>Clinical Note & Disclaimer:</b> <i>This report is generated for informational tracking purposes. "
        "Mild elevation in fasting glycemic parameters and lipid profiles observed. Please correlate clinically "
        "with your primary care physician.</i>"
    )
    story.append(Paragraph(disclaimer, normal_style))

    doc.build(story)
    print(f"Created: {pdf_path}")


def create_sample_csv():
    csv_path = SAMPLES_DIR / "sample_business_sales_analytics.csv"
    np.random.seed(42)
    n = 120

    regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
    categories = ["Enterprise Software", "Cloud Services", "Hardware Devices", "Consulting", "Support Subscriptions"]
    payment_methods = ["Credit Card", "Wire Transfer", "Corporate Net 30", "PayPal"]

    dates = pd.date_range(start="2025-01-01", periods=n, freq="2D").strftime("%Y-%m-%d").tolist()

    data = {
        "Transaction_ID": [f"TX-{1000 + i}" for i in range(n)],
        "Date": dates,
        "Region": np.random.choice(regions, n, p=[0.4, 0.3, 0.2, 0.1]),
        "Product_Category": np.random.choice(categories, n, p=[0.25, 0.35, 0.15, 0.15, 0.10]),
        "Units_Sold": np.random.randint(1, 40, size=n),
        "Unit_Price": np.random.choice([150, 320, 500, 850, 1200, 2400], size=n),
        "Discount_Pct": np.random.choice([0, 5, 10, 15, 20], size=n),
        "Customer_Rating": np.random.choice([3.5, 4.0, 4.2, 4.5, 4.8, 5.0], size=n),
        "Payment_Method": np.random.choice(payment_methods, n),
    }

    df = pd.DataFrame(data)
    # Calculate Revenue and Profit
    df["Gross_Revenue"] = df["Units_Sold"] * df["Unit_Price"]
    df["Net_Revenue"] = (df["Gross_Revenue"] * (1 - df["Discount_Pct"] / 100)).round(2)
    df["Operating_Cost"] = (df["Net_Revenue"] * np.random.uniform(0.40, 0.65, size=n)).round(2)
    df["Net_Profit"] = (df["Net_Revenue"] - df["Operating_Cost"]).round(2)

    df.to_csv(csv_path, index=False)
    print(f"Created: {csv_path}")


if __name__ == "__main__":
    create_sample_marksheet_pdf()
    create_sample_research_paper_pdf()
    create_sample_healthcare_pdf()
    create_sample_csv()
