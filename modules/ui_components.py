from typing import Any
import streamlit as st
from config import DOMAIN_METADATA



def apply_custom_css():
    """Injects custom modern styling into Streamlit."""
    st.markdown("""
    <style>
    /* Main container adjustments */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 96%;
    }

    /* Custom Header Banner */
    .docmind-hero {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 22px 28px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .docmind-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60A5FA, #A78BFA, #F472B6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }
    .docmind-sub {
        color: #94A3B8;
        font-size: 1.05rem;
        margin-bottom: 0px;
    }

    /* Domain Badge Pill */
    .domain-pill {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 8px 18px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 1rem;
        margin: 10px 0;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(96, 165, 250, 0.4);
    }
    .metric-card-title {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-card-value {
        color: #F8FAFC;
        font-size: 1.8rem;
        font-weight: 700;
        line-height: 1.2;
    }
    .metric-card-sub {
        color: #64748B;
        font-size: 0.82rem;
        margin-top: 4px;
    }

    /* Insight Block */
    .insight-box {
        background: rgba(15, 23, 42, 0.7);
        border-left: 4px solid #60A5FA;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: rgba(30, 41, 59, 0.4);
        border-radius: 10px 10px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(59, 130, 246, 0.2) !important;
        border-bottom: 3px solid #3B82F6 !important;
    }

    /* Streamlit chat tweaks */
    .stChatMessage {
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Renders the top title and synopsis subtitle."""
    st.markdown("""
    <div class="docmind-hero">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <div class="docmind-title">⚡ Doc–Mind AI</div>
                <div class="docmind-sub">Multi-Domain Document Intelligence & Dynamic Analytics Platform</div>
            </div>
            <div style="text-align: right; background: rgba(255,255,255,0.06); padding: 8px 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
                <div style="font-size: 0.78rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">JIIT Major Project</div>
                <div style="font-size: 0.9rem; font-weight: 600; color: #E2E8F0;">B.Tech CSE | 15B19CL791</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_domain_badge(domain: str, confidence: float = 0.95, sub_category: str = ""):
    """Renders a colorful glowing domain badge pill."""
    meta = DOMAIN_METADATA.get(domain, DOMAIN_METADATA["General / Business"])
    color = meta["color"]
    icon = meta["icon"]

    st.markdown(f"""
    <div class="domain-pill" style="background: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.15); border: 1px solid {color}; color: #F8FAFC;">
        <span style="font-size: 1.25rem;">{icon}</span>
        <span>Detected Domain: <strong style="color: {color};">{domain}</strong></span>
        <span style="background: rgba(255,255,255,0.12); padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; margin-left: 6px;">
            {int(confidence * 100)}% Confidence
        </span>
        {f'<span style="color: #94A3B8; font-size: 0.85rem; margin-left: 6px;">({sub_category})</span>' if sub_category else ''}
    </div>
    """, unsafe_allow_html=True)


def render_kpi_card(title: str, value: Any, subtitle: str = "", icon: str = "📊"):
    """Renders a single KPI card inside Streamlit column."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-card-title">{icon} {title}</div>
        <div class="metric-card-value">{value}</div>
        <div class="metric-card-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
