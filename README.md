# Doc–Mind AI: Multi-Domain Document Intelligence & Dynamic Analytics Platform

**Jaypee Institute of Information Technology (JIIT)**  
**Major Project — Course Code: 15B19CL791 | B.Tech CSE**  
**Project Team:**  
- **Saksham Chawla** (9923103142)  
- **Mrigank Rai** (9923103126)  
- **Aditya Kumar Gupta** (9923103125)  

---

## 📌 Architectural Vision

**DOC MIND AI** is an AI-powered multi-domain document intelligence and dynamic analytics platform designed to replace generic summarization and rigid dashboards with an **Agentic AI architecture** where:
> **"The document determines the analysis, and the analysis determines the dashboard."**

---

## 💎 Modern Full-Stack Technology Stack

- **Frontend:** Modern **React 18** SPA (built with **Vite**, **Tailwind CSS**, **Lucide-React** icons, and **Recharts**)
  - Sleek **Obsidian Dark & Cyber-Neon** glassmorphism aesthetic
  - Dynamic responsive charts (Bar, Radar, Donut, Area, Range Span)
  - Full-featured conversational RAG chatbot with evidence citation expanders
- **Backend Server:** **FastAPI** (Python 3.11 with Uvicorn)
  - Unified single-port deployment (`http://localhost:8000`) serving both the compiled React frontend and REST API
- **AI & Reasoning Engine:** **Google Gemini API** (`gemini-2.5-flash`, `gemini-1.5-flash`, `gemini-1.5-pro`)
  - Hybrid SDK + pure REST API fallback
- **Document & Data Processing:** PyPDF, Pandas, NumPy, Scikit-Learn TF-IDF vector search, OpenPyXL, ReportLab

---

## 🚀 Key Modules & Deep Analytical Features

### 📄 Tab 1: PDF Intelligence & Dynamic Dashboard
1. **Agentic Multi-Domain Classification**:
   - Automatically determines whether an uploaded document is:
     - 🎓 **Education**: Marksheets, Academic Transcripts, Grade Cards
     - 🔬 **Research**: Academic Papers, Theses, Technical Publications
     - 🩺 **Healthcare**: Diagnostic Panels, Metabolic Profiles, Clinical Assays *(Informational tracking)*
     - 💼 **Finance**: Balance Sheets, Quarterly P&L Filings, Income Statements
     - 📄 **General / Business**: Executive Briefs, Strategy Charters, Corporate Policies
2. **Comprehensive Multi-Paragraph Analytical Summaries**:
   - Exhaustive 3-to-4 paragraph executive evaluations articulating operational context, underlying metrics, strengths, and risk indicators.
3. **Adaptive Visual Dashboards**:
   - **Education:** Subject score bar chart with Pass/Distinction threshold lines, cognitive competency radar map, SWOT strengths & weaknesses, actionable learning roadmap, and career pathway suggestions.
   - **Research:** Quantitative metrics vs baseline comparison bar chart, conceptual taxonomy tree, primary technical findings, theoretical limitations, and future scope.
   - **Healthcare:** Biomarker status distribution donut chart, reference interval span position chart, complete biomarker assay table with biological significance, lifestyle guidance, and targeted doctor discussion points.
   - **Finance:** Financial overview waterfall/bar chart, operating expense allocation donut, top-line revenue metrics, and strategic recommendations.
   - **General:** Key theme relevance weighting bar chart, named entity mapping, and action item roadmap.
4. **Context-Grounded RAG Chatbot**:
   - In-memory vector chunking and sublinear cosine similarity retrieval.
   - Answers grounded in document evidence with expandable source citation cards (Page number & similarity percentage).

### 📊 Tab 2: Excel & CSV Analytics Dashboard
1. **Automated Schema & Statistical Profiling**:
   - Row counts, column types, completeness %, missing cells, and descriptive statistics.
   - Multi-sheet workbook support with active worksheet switcher.
2. **Deep AI Data Story**:
   - Multi-paragraph executive narrative explaining commercial trends, volume concentrations, and business drivers.
3. **Automated Recharts Visualizations Grid**:
   - Parametric distribution histograms
   - Segment breakdown horizontal bar charts
   - Longitudinal time-series trend area charts
4. **Interactive Raw Data Explorer & Export**:
   - Sortable table preview of dataset rows with 1-click CSV download.
5. **Conversational AI Data Analyst**:
   - Natural language spreadsheet Q&A with 1-click suggested question chips.

---

## ⚡ Quick Start

### 1. Launch with One Command:
```bash
cd /Users/mrigankrai/Desktop/doc-mind-ai
./run.sh
```
*The script automatically checks dependencies, compiles the frontend if needed, starts the FastAPI server, and launches `http://localhost:8000` in your browser.*

### 2. Configure Gemini API Key:
Click **"Configure API Key"** in the top navigation bar to insert your key from [Google AI Studio](https://aistudio.google.com/). *(Even in offline mode, the platform operates seamlessly using local rule-based heuristics and vector retrieval).*

### 3. Instant 1-Click Demos:
Use the top sample bar to test verified benchmarks with one click:
- 🎓 **Academic Marksheet** (Education)
- 🔬 **Research Paper** (Research)
- 🩺 **Clinical Lab Report** (Healthcare)
- 📊 **Sales Performance CSV** (Excel Analytics)

---

## 📁 Directory Layout

```
doc-mind-ai/
├── backend/
│   └── server.py               # Unified FastAPI server & REST API
├── frontend/                   # Modern React + Vite + Tailwind SPA
│   ├── src/
│   │   ├── components/         # Navbar, ApiKeyModal, SampleBar, DomainDashboard, RagChatPanel, ExcelDashboard
│   │   ├── App.jsx             # Main React application
│   │   └── index.css           # Custom Glassmorphism & Neon styles
│   ├── dist/                   # Production-compiled assets
│   └── package.json
├── modules/
│   ├── gemini_client.py        # Gemini client with SDK + direct REST fallback
│   ├── pdf_processor.py        # PDF text extractor and chunker
│   ├── rag_engine.py           # In-memory TF-IDF vector similarity search
│   ├── domain_classifier.py    # Agentic multi-domain classifier
│   ├── domain_analyzers/       # Deep domain analyzers (Education, Research, Healthcare, Finance, General)
│   └── excel_analyzer.py       # Excel/CSV profiler, chart generator, and AI data story engine
├── samples/                    # Verified test files & generator
├── run.sh                      # Unified launch script
└── test_suite.py               # Automated smoke test suite
```
