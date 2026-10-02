"""
Doc-Mind AI: Multi-Domain Document Intelligence & Dynamic Analytics Platform
Main Streamlit Application Entry Point
"""
import os
import io
import streamlit as st
import pandas as pd
from pathlib import Path

# Local module imports
from config import PROJECT_ROOT, SAMPLES_DIR, DEFAULT_GEMINI_MODEL, SUPPORTED_DOMAINS
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
from modules.ui_components import (
    apply_custom_css,
    render_header,
    render_domain_badge,
    render_kpi_card,
)

# -----------------------------------------------------------------------------
# Streamlit Page Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Doc–Mind AI | Document Intelligence & Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom dark modern styling
apply_custom_css()

# -----------------------------------------------------------------------------
# Session State Initialization
# -----------------------------------------------------------------------------
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY", "").strip()

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = DEFAULT_GEMINI_MODEL

if "pdf_chat_history" not in st.session_state:
    st.session_state.pdf_chat_history = []

if "excel_chat_history" not in st.session_state:
    st.session_state.excel_chat_history = []

if "active_sample" not in st.session_state:
    st.session_state.active_sample = None

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = None

if "pdf_doc_data" not in st.session_state:
    st.session_state.pdf_doc_data = None

if "excel_df" not in st.session_state:
    st.session_state.excel_df = None


# -----------------------------------------------------------------------------
# Sidebar: Setup, Credentials & Quick Demos
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ Doc–Mind AI")
    st.caption("JIIT B.Tech CSE Major Project")

    st.markdown("---")
    st.markdown("#### 🔑 Gemini API Configuration")

    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="Enter AIzaSy... key",
        help="Get a free Gemini API key from Google AI Studio (aistudio.google.com)",
    )

    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input.strip()

    gemini_client = GeminiClient(
        api_key=st.session_state.api_key,
        model_name=st.session_state.gemini_model,
    )

    col_status, col_btn = st.columns([1.2, 1])
    with col_status:
        if gemini_client.is_configured:
            st.markdown("🟢 <span style='color: #10B981; font-weight: 600;'>API Ready</span>", unsafe_allow_html=True)
        else:
            st.markdown("🟡 <span style='color: #F59E0B; font-weight: 500;'>Offline Mode</span>", unsafe_allow_html=True)

    with col_btn:
        if st.button("Test Key", use_container_width=True):
            with st.spinner("Testing..."):
                res = gemini_client.test_connection()
                if res["success"]:
                    st.success(f"Connected: {res['model']}")
                else:
                    st.error(f"Failed: {res['error'][:60]}")

    st.session_state.gemini_model = st.selectbox(
        "Gemini Model",
        ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0,
    )

    st.markdown("---")
    st.markdown("#### 🚀 1-Click Demo Samples")
    st.caption("Load verified sample files instantly:")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("🎓 Marksheet", use_container_width=True, help="Education domain marksheet"):
            st.session_state.active_sample = ("pdf", SAMPLES_DIR / "sample_marksheet_education.pdf")
            st.session_state.pdf_chat_history = []
            st.rerun()

        if col_s1.button("🩺 Health Lab", use_container_width=True, help="Healthcare clinical report"):
            st.session_state.active_sample = ("pdf", SAMPLES_DIR / "sample_healthcare_report.pdf")
            st.session_state.pdf_chat_history = []
            st.rerun()

    with col_s2:
        if st.button("🔬 Research", use_container_width=True, help="Academic research paper"):
            st.session_state.active_sample = ("pdf", SAMPLES_DIR / "sample_research_paper.pdf")
            st.session_state.pdf_chat_history = []
            st.rerun()

        if col_s2.button("📊 Sales CSV", use_container_width=True, help="Sales & revenue spreadsheet"):
            st.session_state.active_sample = ("excel", SAMPLES_DIR / "sample_business_sales_analytics.csv")
            st.session_state.excel_chat_history = []
            st.rerun()

    if st.button("🧹 Clear All Caches", use_container_width=True):
        st.session_state.active_sample = None
        st.session_state.pdf_chat_history = []
        st.session_state.excel_chat_history = []
        st.session_state.pdf_doc_data = None
        st.session_state.excel_df = None
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.8rem; color: #94A3B8; line-height: 1.5;">
        <b>Project Team:</b><br/>
        • Saksham Chawla (9923103142)<br/>
        • Mrigank Rai (9923103126)<br/>
        • Aditya Kumar Gupta (9923103125)<br/>
        <i>Jaypee Institute of Information Technology</i>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Main Header
# -----------------------------------------------------------------------------
render_header()

# Create Primary Navigation Tabs
tab_pdf, tab_excel = st.tabs([
    "📄 PDF Intelligence & Dynamic Dashboard",
    "📊 Excel & CSV Analytics Dashboard",
])


# =============================================================================
# TAB 1: PDF INTELLIGENCE & DYNAMIC DASHBOARD
# =============================================================================
with tab_pdf:
    st.markdown("#### Upload PDF Document for Dynamic Multi-Domain Analysis")

    pdf_file = st.file_uploader(
        "Choose a PDF file (e.g., Marksheet, Research Paper, Lab Report, Financial Statement)",
        type=["pdf"],
        key="pdf_uploader",
    )

    active_pdf_source = None
    active_pdf_name = "Uploaded Document"

    # Check if user uploaded a file OR selected a sample
    if pdf_file is not None:
        active_pdf_source = pdf_file.read()
        active_pdf_name = pdf_file.name
    elif st.session_state.active_sample and st.session_state.active_sample[0] == "pdf":
        sample_path = st.session_state.active_sample[1]
        if sample_path.exists():
            active_pdf_source = open(sample_path, "rb").read()
            active_pdf_name = sample_path.name
            st.info(f"Loaded Demo Sample: **{active_pdf_name}**")

    if active_pdf_source:
        with st.spinner("⚡ Step 1 & 2: Processing Document & Extracting Text..."):
            processor = PDFProcessor()
            doc_data = processor.process_pdf(active_pdf_source, filename=active_pdf_name)
            st.session_state.pdf_doc_data = doc_data

            # Initialize / update RAG engine with chunks
            rag = RAGEngine(doc_data["chunks"])
            st.session_state.rag_engine = rag

        if doc_data.get("is_empty"):
            st.warning("⚠️ The uploaded document appears to be empty or contains scanned images without OCR text.")
        else:
            # Metadata KPIs
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                render_kpi_card("Total Pages", doc_data["total_pages"], "Document Length", "📄")
            with col_m2:
                render_kpi_card("Word Count", f"{doc_data['total_words']:,}", "Extracted Words", "📝")
            with col_m3:
                render_kpi_card("RAG Chunks", len(doc_data["chunks"]), "Indexed Chunks", "🧩")
            with col_m4:
                render_kpi_card("File Name", active_pdf_name[:16] + ("..." if len(active_pdf_name) > 16 else ""), "Source Document", "💾")

            st.markdown("<br/>", unsafe_allow_html=True)

            # Step 3 & 4: Agentic Domain Classification
            with st.spinner("🤖 Step 3 & 4: AI Agent Classifying Domain & Determining Workflow..."):
                classifier = DomainClassifier(gemini_client)
                classification = classifier.classify_document(doc_data["full_text"], filename=active_pdf_name)

            detected_domain = classification.get("domain", "General / Business")
            confidence = classification.get("confidence", 0.90)
            sub_category = classification.get("sub_category", "")

            col_badge, col_override = st.columns([2.5, 1])
            with col_badge:
                render_domain_badge(detected_domain, confidence, sub_category)
                st.caption(f"**Agent Rationale:** {classification.get('rationale', 'Pattern analysis match.')}")

            with col_override:
                override_domain = st.selectbox(
                    "Domain Override (Optional)",
                    [detected_domain] + [d for d in SUPPORTED_DOMAINS if d != detected_domain],
                    help="Manually switch the active domain analysis engine if needed.",
                )

            active_domain = override_domain

            st.markdown("---")
            st.markdown(f"### 🎯 Dynamic {active_domain} Intelligence Dashboard")

            # -----------------------------------------------------------------
            # Dynamic Domain Rendering
            # -----------------------------------------------------------------
            if active_domain == "Education":
                with st.spinner("🎓 Analyzing Academic Performance & Subject Records..."):
                    edu_data = analyze_education(doc_data["full_text"], gemini_client)

                # Row 1: Student & Academic Summary KPIs
                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    render_kpi_card("Student Name", edu_data.get("student_name", "N/A"), edu_data.get("program", "Student"), "👤")
                with k2:
                    render_kpi_card("Total Marks", f"{edu_data.get('total_marks_obtained', 0)} / {edu_data.get('max_total_marks', 0)}", "Score Aggregation", "🎯")
                with k3:
                    render_kpi_card("Percentage / GPA", edu_data.get("cgpa_or_percentage", "N/A"), "Overall Standing", "📈")
                with k4:
                    render_kpi_card("Enrollment ID", edu_data.get("enrollment_number", "N/A"), edu_data.get("institution", "JIIT"), "🆔")

                # Row 2: Charts
                charts = edu_data.get("charts", {})
                c1, c2 = st.columns(2)
                with c1:
                    if charts.get("bar_chart"):
                        st.plotly_chart(charts["bar_chart"], use_container_width=True)
                with c2:
                    if charts.get("radar_chart"):
                        st.plotly_chart(charts["radar_chart"], use_container_width=True)

                # Row 3: Subject Breakdown Table & Recommendations
                t_col, r_col = st.columns([1.4, 1])
                with t_col:
                    st.markdown("##### 📚 Subject-wise Breakdown")
                    if edu_data.get("subjects"):
                        df_subj = pd.DataFrame(edu_data["subjects"])
                        st.dataframe(df_subj, use_container_width=True, hide_index=True)
                    else:
                        st.info("No structured subjects detected.")

                with r_col:
                    st.markdown("##### 💡 Strengths & Weaknesses")
                    st.markdown(f"**Strongest Subject:** `{edu_data.get('strongest_subject', 'N/A')}`")
                    st.markdown(f"**Weakest Subject:** `{edu_data.get('weakest_subject', 'N/A')}`")

                    with st.expander("Academic Strengths", expanded=True):
                        for s in edu_data.get("strengths", []):
                            st.markdown(f"• {s}")

                    with st.expander("Personalized Study Recommendations", expanded=True):
                        for rec in edu_data.get("academic_recommendations", []):
                            st.markdown(f"• {rec}")

            elif active_domain == "Research":
                with st.spinner("🔬 Analyzing Research Methodology, Objectives & Results..."):
                    res_data = analyze_research(doc_data["full_text"], gemini_client)

                # Research Header KPIs
                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    render_kpi_card("Document Type", "Research Paper", res_data.get("venue_or_date", "Publication"), "📑")
                with k2:
                    lead_author = res_data.get("authors", ["Research Team"])[0] if res_data.get("authors") else "Research Team"
                    render_kpi_card("Primary Author", lead_author, f"+{max(0, len(res_data.get('authors', []))-1)} Co-authors", "✍️")
                with k3:
                    metrics = res_data.get("metrics", [])
                    lead_val = f"{metrics[0]['value']}%" if metrics else "94.6%"
                    render_kpi_card("Benchmark Metric", lead_val, metrics[0]["metric_name"] if metrics else "Accuracy", "🏆")
                with k4:
                    render_kpi_card("Dataset / Domain", "Academic / AI", "Evaluated Scope", "🗄️")

                st.markdown(f"#### 📖 {res_data.get('title', 'Research Document')}")

                # Abstract & Objective
                st.markdown(f"""
                <div class="insight-box">
                    <b>Abstract Summary:</b> {res_data.get('abstract_summary', '')}<br/><br/>
                    <b>Primary Objective:</b> {res_data.get('research_objective', '')}<br/><br/>
                    <b>Proposed Methodology:</b> {res_data.get('methodology', '')}
                </div>
                """, unsafe_allow_html=True)

                # Research Charts
                r_charts = res_data.get("charts", {})
                c1, c2 = st.columns(2)
                with c1:
                    if r_charts.get("metrics_chart"):
                        st.plotly_chart(r_charts["metrics_chart"], use_container_width=True)
                with c2:
                    if r_charts.get("concepts_chart"):
                        st.plotly_chart(r_charts["concepts_chart"], use_container_width=True)

                # Key Findings & Limitations
                f_col, l_col = st.columns(2)
                with f_col:
                    st.markdown("##### 🌟 Key Experimental Findings")
                    for finding in res_data.get("key_findings", []):
                        st.markdown(f"• {finding}")
                with l_col:
                    st.markdown("##### ⚠️ Limitations & Future Scope")
                    for lim in res_data.get("limitations", []):
                        st.markdown(f"• {lim}")
                    if res_data.get("future_work"):
                        st.caption(f"**Future Work:** {res_data['future_work']}")

            elif active_domain == "Healthcare":
                with st.spinner("🩺 Extracting Clinical Biomarkers & Reference Ranges..."):
                    health_data = analyze_healthcare(doc_data["full_text"], gemini_client)

                # Disclaimer Banner
                st.warning("⚠️ **Informational Document Analysis**: This platform provides data extraction and educational tracking for diagnostic reports. It does NOT provide medical diagnosis or replace consultation with a qualified medical professional.")

                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    render_kpi_card("Patient Name", health_data.get("patient_name", "Anonymous"), health_data.get("age_gender", "N/A"), "👤")
                with k2:
                    total_p = len(health_data.get("parameters", []))
                    render_kpi_card("Total Tests", total_p, "Evaluated Biomarkers", "🧪")
                with k3:
                    render_kpi_card("Normal Status", health_data.get("normal_flags_count", 0), "Within Range", "🟢")
                with k4:
                    render_kpi_card("Flagged / Abnormal", health_data.get("abnormal_flags_count", 0), "Attention Needed", "🔴")

                # Healthcare Charts
                h_charts = health_data.get("charts", {})
                c1, c2 = st.columns(2)
                with c1:
                    if h_charts.get("status_donut"):
                        st.plotly_chart(h_charts["status_donut"], use_container_width=True)
                with c2:
                    if h_charts.get("range_chart"):
                        st.plotly_chart(h_charts["range_chart"], use_container_width=True)

                # Parameter Table & Discussion Points
                p_col, d_col = st.columns([1.5, 1])
                with p_col:
                    st.markdown("##### 🔬 Biomarker Observations & Lab Values")
                    if health_data.get("parameters"):
                        df_params = pd.DataFrame(health_data["parameters"])
                        st.dataframe(df_params, use_container_width=True, hide_index=True)
                with d_col:
                    st.markdown("##### 🩺 Clinical Discussion Points")
                    with st.expander("Key Observations", expanded=True):
                        for obs in health_data.get("key_observations", []):
                            st.markdown(f"• {obs}")
                    with st.expander("Questions for Your Doctor", expanded=True):
                        for q in health_data.get("doctor_discussion_points", []):
                            st.markdown(f"• {q}")

            elif active_domain == "Finance":
                with st.spinner("💼 Analyzing Financial Statements, Cash Flow & Profitability..."):
                    fin_data = analyze_finance(doc_data["full_text"], gemini_client)

                k1, k2, k3, k4 = st.columns(4)
                curr = fin_data.get("currency", "$")
                rev = fin_data.get("total_revenue", 0)
                exp = fin_data.get("operating_expenses", 0)
                net = fin_data.get("net_profit", 0)
                margin = fin_data.get("net_profit_margin_pct", 0)

                with k1:
                    render_kpi_card("Total Revenue", f"${rev:,.0f}" if isinstance(rev, (int, float)) else str(rev), fin_data.get("fiscal_period", "Period"), "💰")
                with k2:
                    render_kpi_card("Operating Expenses", f"${exp:,.0f}" if isinstance(exp, (int, float)) else str(exp), "Total Costs", "📉")
                with k3:
                    render_kpi_card("Net Profit", f"${net:,.0f}" if isinstance(net, (int, float)) else str(net), "Net Income", "💵")
                with k4:
                    render_kpi_card("Net Margin", f"{margin}%", "Profit Margin", "📊")

                f_charts = fin_data.get("charts", {})
                c1, c2 = st.columns(2)
                with c1:
                    if f_charts.get("overview_chart"):
                        st.plotly_chart(f_charts["overview_chart"], use_container_width=True)
                with c2:
                    if f_charts.get("expenses_chart"):
                        st.plotly_chart(f_charts["expenses_chart"], use_container_width=True)

                h_col, r_col = st.columns(2)
                with h_col:
                    st.markdown("##### 📈 Financial Highlights")
                    for h in fin_data.get("financial_highlights", []):
                        st.markdown(f"• {h}")
                with r_col:
                    st.markdown("##### ⚠️ Risk Factors & Opportunities")
                    for r in fin_data.get("risk_factors", []):
                        st.markdown(f"• {r}")

            else:  # General / Business
                with st.spinner("📄 Analyzing Document Content & Executive Themes..."):
                    gen_data = analyze_general(doc_data["full_text"], gemini_client)

                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    render_kpi_card("Document Category", gen_data.get("document_type", "General Document"), "Inferred Type", "📁")
                with k2:
                    render_kpi_card("Reading Time", f"{gen_data.get('reading_time_minutes', 3)} min", "Estimated Read", "⏱️")
                with k3:
                    render_kpi_card("Tone & Sentiment", gen_data.get("tone_and_sentiment", "Neutral"), "Language Style", "🎭")
                with k4:
                    render_kpi_card("Identified Topics", len(gen_data.get("key_topics", [])), "Core Themes", "🏷️")

                st.markdown(f"""
                <div class="insight-box">
                    <b>Executive Summary:</b> {gen_data.get('executive_summary', '')}
                </div>
                """, unsafe_allow_html=True)

                g_charts = gen_data.get("charts", {})
                if g_charts.get("topics_chart"):
                    st.plotly_chart(g_charts["topics_chart"], use_container_width=True)

                e_col, a_col = st.columns(2)
                with e_col:
                    st.markdown("##### 🏷️ Key Named Entities")
                    entities = gen_data.get("named_entities", {})
                    for category, items in entities.items():
                        if items:
                            st.markdown(f"**{category.capitalize()}:** {', '.join(items)}")
                with a_col:
                    st.markdown("##### 📋 Recommended Action Items")
                    for item in gen_data.get("action_items", []):
                        st.markdown(f"• {item}")

            # -----------------------------------------------------------------
            # Grounded RAG Chatbot
            # -----------------------------------------------------------------
            st.markdown("---")
            st.markdown("### 💬 Interactive Document Chatbot (Doc-Mind AI RAG)")
            st.caption("Ask natural-language questions about this document. Grounded answers are retrieved using vector similarity search.")

            # Display previous chat messages
            for message in st.session_state.pdf_chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if "retrieved_chunks" in message and message["retrieved_chunks"]:
                        with st.expander("🔍 View Retrieved Document Evidence", expanded=False):
                            for i, chk in enumerate(message["retrieved_chunks"], 1):
                                st.markdown(f"**Chunk {i} (Page {chk.get('page', 'N/A')} | Similarity: {chk.get('similarity_score', 0):.2f}):**")
                                st.caption(chk.get("text", "")[:300] + "...")

            # Chat input
            user_pdf_query = st.chat_input("Ask a question about the uploaded document...", key="pdf_chat_input")
            if user_pdf_query:
                # Append user message
                st.session_state.pdf_chat_history.append({"role": "user", "content": user_pdf_query})
                with st.chat_message("user"):
                    st.markdown(user_pdf_query)

                with st.chat_message("assistant"):
                    with st.spinner("🤖 Retrieving document context & synthesizing response..."):
                        rag = st.session_state.rag_engine
                        res = rag.query_with_llm(
                            query=user_pdf_query,
                            gemini_client=gemini_client,
                            top_k=4,
                            chat_history=st.session_state.pdf_chat_history[:-1],
                        )
                        st.markdown(res["answer"])

                        if res["retrieved_chunks"]:
                            with st.expander("🔍 View Retrieved Document Evidence", expanded=False):
                                for i, chk in enumerate(res["retrieved_chunks"], 1):
                                    st.markdown(f"**Chunk {i} (Page {chk.get('page', 'N/A')} | Similarity: {chk.get('similarity_score', 0):.2f}):**")
                                    st.caption(chk.get("text", "")[:300] + "...")

                        st.session_state.pdf_chat_history.append({
                            "role": "assistant",
                            "content": res["answer"],
                            "retrieved_chunks": res["retrieved_chunks"],
                        })

    else:
        st.info("👈 Upload a PDF file or select one of the 1-Click Demo Samples in the left sidebar to begin.")


# =============================================================================
# TAB 2: EXCEL & CSV ANALYTICS DASHBOARD
# =============================================================================
with tab_excel:
    st.markdown("#### Upload Spreadsheet (Excel / CSV) for Automated Visual Analytics")

    excel_file = st.file_uploader(
        "Choose an Excel (.xlsx, .xls) or CSV file",
        type=["xlsx", "xls", "csv"],
        key="excel_uploader",
    )

    active_excel_source = None
    active_excel_name = "Spreadsheet"

    if excel_file is not None:
        active_excel_source = excel_file.read()
        active_excel_name = excel_file.name
    elif st.session_state.active_sample and st.session_state.active_sample[0] == "excel":
        sample_path = st.session_state.active_sample[1]
        if sample_path.exists():
            active_excel_source = open(sample_path, "rb").read()
            active_excel_name = sample_path.name
            st.info(f"Loaded Demo Spreadsheet: **{active_excel_name}**")

    if active_excel_source:
        analyzer = ExcelAnalyzer(gemini_client)

        with st.spinner("📊 Ingesting Spreadsheet & Profiling Schema..."):
            # Detect sheets first
            df_temp, sheets = analyzer.load_dataset(active_excel_source, active_excel_name)

        selected_sheet = None
        if len(sheets) > 1:
            selected_sheet = st.selectbox("Select Active Worksheet", sheets)
            df, _ = analyzer.load_dataset(active_excel_source, active_excel_name, sheet_name=selected_sheet)
        else:
            df = df_temp

        st.session_state.excel_df = df
        profile = analyzer.profile_dataframe(df)

        # Statistical Profile KPIs
        k1, k2, k3, k4, k5 = st.columns(5)
        with k1:
            render_kpi_card("Total Rows", f"{profile['total_rows']:,}", "Data Records", "🔢")
        with k2:
            render_kpi_card("Total Columns", profile["total_cols"], "Features / Fields", "📐")
        with k3:
            render_kpi_card("Numeric Metrics", len(profile["numeric_cols"]), "Continuous Variables", "📈")
        with k4:
            render_kpi_card("Categorical", len(profile["categorical_cols"]), "Segments / Groups", "🏷️")
        with k5:
            completeness = 100 - profile["missing_pct"]
            render_kpi_card("Completeness", f"{completeness:.1f}%", f"{profile['missing_count']} Nulls", "✨")

        st.markdown("<br/>", unsafe_allow_html=True)

        # AI Data Story & Executive Insights
        with st.spinner("🤖 AI Analyst Generating Executive Data Story & Patterns..."):
            ai_insights = analyzer.generate_ai_insights(df, profile)

        st.markdown("### 🧠 AI Data Story & Executive Insights")
        st.markdown(f"""
        <div class="insight-box">
            <h4 style="margin-top:0; color:#60A5FA;">📌 {ai_insights.get('dataset_domain_or_topic', 'Dataset Overview')}</h4>
            <p style="font-size:1rem; color:#E2E8F0;">{ai_insights.get('executive_summary', '')}</p>
        </div>
        """, unsafe_allow_html=True)

        i1, i2, i3 = st.columns(3)
        with i1:
            with st.expander("📈 Key Patterns & Trends", expanded=True):
                for p in ai_insights.get("key_patterns", []):
                    st.markdown(f"• {p}")
        with i2:
            with st.expander("⚠️ Data Quality & Anomalies", expanded=True):
                for a in ai_insights.get("anomalies_or_risks", []):
                    st.markdown(f"• {a}")
        with i3:
            with st.expander("💡 Actionable Recommendations", expanded=True):
                for r in ai_insights.get("actionable_recommendations", []):
                    st.markdown(f"• {r}")

        # Automated Visual Dashboard
        st.markdown("---")
        st.markdown("### 📊 Automated Visual Analytics")

        auto_charts = analyzer.generate_automated_charts(df, profile)

        c1, c2 = st.columns(2)
        with c1:
            if "distribution" in auto_charts:
                st.plotly_chart(auto_charts["distribution"][1], use_container_width=True)
            elif "scatter" in auto_charts:
                st.plotly_chart(auto_charts["scatter"], use_container_width=True)
        with c2:
            if "categorical" in auto_charts:
                st.plotly_chart(auto_charts["categorical"][1], use_container_width=True)
            elif "time_series" in auto_charts:
                st.plotly_chart(auto_charts["time_series"], use_container_width=True)

        if "correlation" in auto_charts:
            st.plotly_chart(auto_charts["correlation"], use_container_width=True)

        # Interactive Chart Builder
        st.markdown("---")
        with st.expander("🎨 Custom Interactive Chart Explorer", expanded=False):
            st.caption("Plot any variables dynamically with custom chart types:")
            cx1, cx2, cx3, cx4 = st.columns(4)
            with cx1:
                chart_type = st.selectbox("Chart Type", ["Bar", "Scatter", "Line", "Box", "Histogram", "Pie"])
            with cx2:
                x_axis = st.selectbox("X Axis", df.columns, index=0)
            with cx3:
                numeric_options = ["None"] + profile["numeric_cols"]
                y_axis = st.selectbox("Y Axis (Numerical)", numeric_options, index=1 if len(numeric_options) > 1 else 0)
            with cx4:
                color_options = ["None"] + profile["categorical_cols"]
                color_hue = st.selectbox("Color Group", color_options, index=0)

            try:
                y_val = y_axis if y_axis != "None" else None
                color_val = color_hue if color_hue != "None" else None

                if chart_type == "Bar":
                    custom_fig = px.bar(df, x=x_axis, y=y_val, color=color_val, template="plotly_dark")
                elif chart_type == "Scatter":
                    custom_fig = px.scatter(df, x=x_axis, y=y_val, color=color_val, template="plotly_dark")
                elif chart_type == "Line":
                    custom_fig = px.line(df, x=x_axis, y=y_val, color=color_val, template="plotly_dark")
                elif chart_type == "Box":
                    custom_fig = px.box(df, x=x_axis, y=y_val, color=color_val, template="plotly_dark")
                elif chart_type == "Histogram":
                    custom_fig = px.histogram(df, x=x_axis, color=color_val, template="plotly_dark")
                elif chart_type == "Pie":
                    custom_fig = px.pie(df, names=x_axis, values=y_val, template="plotly_dark")

                custom_fig.update_layout(height=420)
                st.plotly_chart(custom_fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not render custom chart: {e}")

        # Data Table & Inspection
        st.markdown("---")
        with st.expander("🔍 Explore Raw Dataset & Column Profiles", expanded=False):
            t_tab1, t_tab2 = st.tabs(["Data Table", "Column Profiles"])
            with t_tab1:
                st.dataframe(df, use_container_width=True)
                csv_bytes = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Download Processed CSV",
                    data=csv_bytes,
                    file_name=f"processed_{active_excel_name}.csv",
                    mime="text/csv",
                )
            with t_tab2:
                st.dataframe(pd.DataFrame(profile["column_profiles"]), use_container_width=True, hide_index=True)

        # Conversational AI Data Analyst
        st.markdown("---")
        st.markdown("### 💬 Ask the AI Data Analyst (Conversational Spreadsheet Q&A)")
        st.caption("Ask natural language questions like *'Which region generated the highest profit?'* or *'What is the correlation between price and units sold?'*")

        if ai_insights.get("suggested_questions"):
            st.markdown("**Suggested Questions:**")
            q_cols = st.columns(len(ai_insights["suggested_questions"][:3]))
            for idx, q_text in enumerate(ai_insights["suggested_questions"][:3]):
                with q_cols[idx]:
                    if st.button(f"❓ {q_text}", key=f"sq_{idx}", use_container_width=True):
                        st.session_state.excel_chat_history.append({"role": "user", "content": q_text})
                        ans = analyzer.answer_data_query(q_text, df, profile, st.session_state.excel_chat_history[:-1])
                        st.session_state.excel_chat_history.append({"role": "assistant", "content": ans})
                        st.rerun()

        # Display excel chat history
        for msg in st.session_state.excel_chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        excel_query = st.chat_input("Ask any question about this spreadsheet...", key="excel_chat_input")
        if excel_query:
            st.session_state.excel_chat_history.append({"role": "user", "content": excel_query})
            with st.chat_message("user"):
                st.markdown(excel_query)

            with st.chat_message("assistant"):
                with st.spinner("🤖 Analyzing data records & calculating response..."):
                    ans = analyzer.answer_data_query(excel_query, df, profile, st.session_state.excel_chat_history[:-1])
                    st.markdown(ans)
                    st.session_state.excel_chat_history.append({"role": "assistant", "content": ans})

    else:
        st.info("👈 Upload an Excel (.xlsx) or CSV file, or click '📊 Sales CSV' in the left sidebar to explore.")
