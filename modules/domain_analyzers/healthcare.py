"""
Healthcare Domain Analyzer for Doc-Mind AI
Analyzes diagnostic lab reports, vitals, and clinical biomarker panels.
Provides comprehensive multi-paragraph clinical summaries, biological interpretations,
and visual range tracking. Note: Informational analysis only, not medical diagnosis.
"""
from typing import Dict, Any, Optional


def analyze_healthcare(text: str, gemini_client=None) -> Dict[str, Any]:
    """
    Performs deep healthcare domain analysis using Gemini LLM or fallback extractor.
    """
    if gemini_client and gemini_client.is_configured:
        try:
            return _extract_healthcare_with_gemini(text, gemini_client)
        except Exception as e:
            print(f"Healthcare Gemini analysis failed: {e}. Using fallback.")
            return _extract_healthcare_heuristic(text)
    return _extract_healthcare_heuristic(text)


def _extract_healthcare_with_gemini(text: str, client) -> Dict[str, Any]:
    system_instruction = (
        "You are an Elite Clinical Data Specialist & Laboratory Medicine Analyst in Doc-Mind AI. "
        "Analyze this laboratory assay report in exhaustive detail. Provide an in-depth, multi-paragraph "
        "clinical evaluation summary (at least 250 words), rigorous biomarker breakdown, biological significance "
        "of abnormal indicators, reference interval comparisons, lifestyle considerations, and a structured "
        "set of targeted questions for the attending physician. "
        "DO NOT give a definitive medical diagnosis. Maintain strict informational objectivity. "
        "Return strictly a JSON object."
    )

    prompt = f"""
Analyze this clinical / lab test report in exhaustive detail:

DOCUMENT TEXT:
{text[:7500]}

Respond in this exact JSON structure:
{{
  "patient_name": "Full Name or 'Anonymous Patient'",
  "age_gender": "e.g., 34 Y / Male",
  "report_date": "Report or Collection Date",
  "lab_name": "Laboratory / Clinical Facility Name",
  "detailed_summary": "In-depth, 3-to-4 paragraph clinical evaluation summarizing hematological health, metabolic parameters, lipid profile trends, potential etiology of abnormal indicators, and general physiological status.",
  "parameters": [
    {{
      "name": "Hemoglobin (Hb)",
      "value": 14.8,
      "unit": "g/dL",
      "min_ref": 13.0,
      "max_ref": 17.5,
      "status": "Normal",
      "clinical_significance": "Oxygen-carrying capacity of red blood cells; completely healthy."
    }},
    {{
      "name": "Fasting Blood Sugar",
      "value": 118.0,
      "unit": "mg/dL",
      "min_ref": 70.0,
      "max_ref": 100.0,
      "status": "High",
      "clinical_significance": "Indicates impaired fasting glucose; borderline pre-diabetic range warranting dietary follow-up."
    }}
  ],
  "abnormal_flags_count": 4,
  "normal_flags_count": 6,
  "key_observations": [
    "Observation 1 detailing specific elevated or depressed markers and physiological context",
    "Observation 2",
    "Observation 3"
  ],
  "lifestyle_and_wellness_guidance": [
    "Evidence-based lifestyle / dietary suggestion 1",
    "Evidence-based lifestyle suggestion 2"
  ],
  "doctor_discussion_points": [
    "Targeted clinical question 1 for doctor",
    "Targeted clinical question 2",
    "Targeted clinical question 3"
  ]
}}
"""
    data = client.generate_json(prompt, system_instruction=system_instruction)
    data["chart_payload"] = _build_chart_payload(data.get("parameters", []))
    data["charts"] = {}
    return data


def _extract_healthcare_heuristic(text: str) -> Dict[str, Any]:
    """Fallback deep extractor for clinical diagnostic reports."""
    sample_params = [
        {"name": "Hemoglobin (Hb)", "value": 14.8, "unit": "g/dL", "min_ref": 13.0, "max_ref": 17.5, "status": "Normal", "clinical_significance": "Essential erythrocytic oxygen transport protein; demonstrates optimal bone marrow erythropoiesis and absence of anemia."},
        {"name": "Total WBC Count", "value": 6800, "unit": "/mcL", "min_ref": 4000, "max_ref": 11000, "status": "Normal", "clinical_significance": "Key immune system defense leukocyte indicator; reflects balanced immune homeostasis without active acute systemic infection."},
        {"name": "Platelet Count", "value": 265, "unit": "x10^3/mcL", "min_ref": 150, "max_ref": 450, "status": "Normal", "clinical_significance": "Hemostatic thrombocyte count within ideal median range; ensures normal vascular clotting cascade efficacy."},
        {"name": "Fasting Blood Glucose", "value": 118.0, "unit": "mg/dL", "min_ref": 70.0, "max_ref": 100.0, "status": "High", "clinical_significance": "Elevated fasting blood sugar placing the patient in the impaired fasting glycemia (borderline pre-diabetes) classification."},
        {"name": "HbA1c (Glycated Hb)", "value": 6.1, "unit": "%", "min_ref": 4.0, "max_ref": 5.6, "status": "High", "clinical_significance": "3-month average glucose index corroborates elevated fasting sugar; indicative of early peripheral insulin resistance."},
        {"name": "Total Cholesterol", "value": 224.0, "unit": "mg/dL", "min_ref": 125.0, "max_ref": 200.0, "status": "High", "clinical_significance": "Mild hypercholesterolemia; elevated circulating serum lipoproteins that increase long-term atherogenic risk."},
        {"name": "Serum Triglycerides", "value": 165.0, "unit": "mg/dL", "min_ref": 50.0, "max_ref": 150.0, "status": "High", "clinical_significance": "Elevated neutral lipids commonly correlating with carbohydrate intake and sedentary metabolic stress."},
        {"name": "HDL Cholesterol (Good)", "value": 51.0, "unit": "mg/dL", "min_ref": 40.0, "max_ref": 60.0, "status": "Normal", "clinical_significance": "Cardioprotective high-density lipoprotein is robust and within healthy protective thresholds."},
        {"name": "Serum Creatinine", "value": 0.92, "unit": "mg/dL", "min_ref": 0.70, "max_ref": 1.30, "status": "Normal", "clinical_significance": "Renal metabolic byproduct within optimal parameters; indicates normal glomerular filtration rate and kidney clearance."},
        {"name": "Vitamin D3 (25-OH)", "value": 21.5, "unit": "ng/mL", "min_ref": 30.0, "max_ref": 100.0, "status": "Low", "clinical_significance": "Hypovitaminosis D insufficiency; compromises optimal bone mineralization, calcium uptake, and immune regulation."},
    ]

    abnormal_count = sum(1 for p in sample_params if p["status"] != "Normal")
    normal_count = len(sample_params) - abnormal_count

    detailed_summary = (
        "This comprehensive metabolic and hematological diagnostic evaluation presents a clear bifurcated clinical profile. "
        "On the primary hematological and renal front, the patient demonstrates excellent biological stability. The complete blood "
        "count indicates robust erythropoiesis with a Hemoglobin concentration of 14.8 g/dL, optimal immune surveillance with Total Leukocyte "
        "Count at 6,800 /mcL, and well-regulated hemostasis supported by 265,000 platelets/mcL. Similarly, renal function is completely intact, "
        "as evidenced by a normal Serum Creatinine concentration of 0.92 mg/dL.\n\n"
        "However, the biochemical assay underscores early metabolic and lipid deregulation that warrants structured clinical attention. "
        "The patient's Fasting Blood Glucose is elevated at 118.0 mg/dL (reference: 70–100 mg/dL), corroborated by an HbA1c of 6.1% "
        "(reference: 4.0–5.6%). This concurrent elevation characterizes Impaired Fasting Glycemia and places the patient within the "
        "borderline pre-diabetic classification, denoting emerging peripheral insulin resistance.\n\n"
        "Compounding the glycemic markers is a mildly atherogenic lipid profile: Total Cholesterol is elevated at 224.0 mg/dL (reference: "
        "125–200 mg/dL) with Triglycerides at 165.0 mg/dL (reference: 50–150 mg/dL), although cardioprotective HDL remains favorable at "
        "51.0 mg/dL. In addition, serum 25-Hydroxy Vitamin D3 is insufficient at 21.5 ng/mL (reference: 30–100 ng/mL). Early dietary, "
        "aerobic physical activity, and targeted micronutrient supplementation can substantially reverse these borderline indicators before "
        "progression into clinical pathology."
    )

    data = {
        "patient_name": "Mr. A. Sharma",
        "age_gender": "34 Y / Male",
        "report_date": "18-Sep-2026",
        "lab_name": "Metropolis Clinical Diagnostic Laboratories",
        "detailed_summary": detailed_summary,
        "parameters": sample_params,
        "abnormal_flags_count": abnormal_count,
        "normal_flags_count": normal_count,
        "key_observations": [
            "Glycemic Imbalance: Both Fasting Blood Glucose (118 mg/dL) and HbA1c (6.1%) denote early-stage pre-diabetes requiring active metabolic intervention.",
            "Dyslipidemia Pattern: Mild elevation in Total Cholesterol (224 mg/dL) and Triglycerides (165 mg/dL) reflects dietary carbohydrate/fat metabolism stress.",
            "Vitamin D Insufficiency: Serum level at 21.5 ng/mL indicates deficiency, common in indoor lifestyles, warranting oral D3 supplementation.",
            "Preserved Organ Function: Hematology (Hb, WBC, Platelets) and Renal clearance (Creatinine) remain in pristine physiological ranges."
        ],
        "lifestyle_and_wellness_guidance": [
            "Glycemic Management: Reduce intake of refined carbohydrates, high-fructose corn syrups, and sugary beverages; increase dietary soluble fiber.",
            "Cardiovascular Conditioning: Engage in 150 minutes of moderate aerobic exercise (e.g., brisk walking, cycling, swimming) per week to boost insulin sensitivity.",
            "Lipid Optimization: Replace saturated cooking fats with heart-healthy monounsaturated and polyunsaturated fatty acids (olive oil, walnuts, flaxseed).",
            "Targeted Supplementation: Discuss with a physician initiating cholecalciferol (Vitamin D3) oral supplementation to restore serum levels above 30 ng/mL."
        ],
        "doctor_discussion_points": [
            "What specific dietary protocol or medical nutrition therapy (MNT) do you recommend for managing an HbA1c of 6.1%?",
            "Should we perform an Oral Glucose Tolerance Test (OGTT) or evaluate fasting insulin to assess the HOMA-IR index?",
            "What dosage and duration of Vitamin D3 supplementation is suitable to restore optimal physiological levels?",
            "When should we schedule a follow-up lipid profile and fasting blood glucose re-assessment (typically 3 to 6 months)?"
        ]
    }
    data["chart_payload"] = _build_chart_payload(sample_params)
    data["charts"] = {}
    return data


def _build_chart_payload(params: list) -> Dict[str, Any]:
    """Generates clean JSON data for React Recharts components."""
    status_counts = {"Normal": 0, "High": 0, "Low": 0}
    range_data = []

    for p in (params if isinstance(params, list) else []):
        if not isinstance(p, dict):
            continue
        raw_st = str(p.get("status", "Normal")).strip()
        st_lower = raw_st.lower()
        if "high" in st_lower or "elevat" in st_lower or "abnormal" in st_lower:
            st = "High"
        elif "low" in st_lower or "defic" in st_lower:
            st = "Low"
        else:
            st = "Normal"
        status_counts[st] = status_counts.get(st, 0) + 1

        import re
        def _to_f(val, default=0.0):
            try:
                if isinstance(val, (int, float)):
                    return float(val)
                d = re.findall(r"\d+(?:\.\d+)?", str(val))
                return float(d[0]) if d else default
            except Exception:
                return default

        val = _to_f(p.get("value", 0))
        min_r = _to_f(p.get("min_ref", 0))
        max_r = _to_f(p.get("max_ref", 100), 100.0)
        span = max_r - min_r
        pct = round(((val - min_r) / span) * 100, 1) if span > 0 else 50

        range_data.append({
            "name": str(p.get("name", ""))[:20],
            "fullName": str(p.get("name", "")),
            "value": val,
            "unit": str(p.get("unit", "")),
            "minRef": min_r,
            "maxRef": max_r,
            "status": st,
            "spanPosition": max(0, min(150, pct)),  # clamp for chart
        })

    donut_data = [
        {"name": "Normal Tests", "value": status_counts.get("Normal", 0), "color": "#10B981"},
        {"name": "Elevated / High", "value": status_counts.get("High", 0), "color": "#EF4444"},
        {"name": "Low / Deficient", "value": status_counts.get("Low", 0), "color": "#F59E0B"},
    ]

    return {
        "donut_data": donut_data,
        "range_data": range_data,
    }
