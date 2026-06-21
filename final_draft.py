"""
Age Check — Boolean Privacy Demo
A premium, production-grade Streamlit application.

Run:  streamlit run app.py
"""

import io
import math
import random
from datetime import datetime

import cv2
import numpy as np
import pandas as pd
import io
import math
import random
from datetime import datetime

import cv2
import numpy as np
import pandas as pd
import requests

from app.main import calculate_confidence 

API_URL = "http://127.0.0.1:8000/check_age"
API_TOKEN = "age-check-api-token-2026"

import streamlit as st
from PIL import Image

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG — must be the very first Streamlit call
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AgeGuard · Boolean Privacy",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# DEEP STYLE — Space Grotesk + Inter, dark glass design system
# ─────────────────────────────────────────────────────────────────────────────
GLOBAL_CSS = """
/* ── Google Fonts ─────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Design tokens ────────────────────────────────────────────────────── */
:root {
  --bg:          #070D1A;
  --surface:     #0D1527;
  --surface-2:   #111E35;
  --surface-3:   #172440;
  --border:      #1E2F4D;
  --border-glow: #2563EB44;
  --accent:      #2563EB;
  --accent-2:    #3B82F6;
  --accent-glow: #2563EB22;
  --success:     #10B981;
  --warning:     #F59E0B;
  --danger:      #EF4444;
  --text-1:      #F0F6FF;
  --text-2:      #94A3C8;
  --text-3:      #5B6E99;
  --font-display:'Space Grotesk', sans-serif;
  --font-body:   'Inter', sans-serif;
  --font-mono:   'JetBrains Mono', monospace;
  --radius:      12px;
  --radius-lg:   18px;
}

/* ── Reset & base ─────────────────────────────────────────────────────── */
html, body, .stApp { background: var(--bg) !important; }
*, *::before, *::after { box-sizing: border-box; }

/* ── Kill Streamlit chrome ────────────────────────────────────────────── */
#MainMenu,
footer{
    visibility: hidden;
}    
.block-container {
  padding: 0 2.5rem 3rem !important;
  max-width: 1280px !important;
}

/* ── Sidebar ──────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
section[data-testid="stSidebar"] * { color: var(--text-2) !important; }
section[data-testid="stSidebar"] .stMarkdown h3 {
  color: var(--text-1) !important;
  font-family: var(--font-display) !important;
}

/* ── Typography ───────────────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-display) !important;
  color: var(--text-1) !important;
  letter-spacing: -0.02em;
}
p, li {
    font-family: var(--font-body) !important;
    color: var(--text-2) !important;
}

label {
    font-family: var(--font-body) !important;
    color: var(--text-2) !important;
}

/* ── Streamlit widget labels ──────────────────────────────────────────── */
.stSelectbox label, .stMultiSelect label,
.stSlider label, .stNumberInput label,
.stTextInput label, .stFileUploader label,
.stRadio label, .stCheckbox label {
  font-family: var(--font-display) !important;
  font-size: 0.78rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
  color: var(--text-3) !important;
}

/* ── Inputs ───────────────────────────────────────────────────────────── */
.stTextInput input, .stNumberInput input,
.stTextArea textarea {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-1) !important;
  font-family: var(--font-body) !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* ── Select / Multiselect ─────────────────────────────────────────────── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-1) !important;
}

/* ── Slider ───────────────────────────────────────────────────────────── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
  background: var(--accent) !important;
}

/* ── Buttons ──────────────────────────────────────────────────────────── */
.stButton > button {
  background: var(--accent) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--radius) !important;
  font-family: var(--font-display) !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  letter-spacing: 0.01em !important;
  padding: 0.65rem 1.5rem !important;
  transition: all .2s ease !important;
  box-shadow: 0 4px 14px #2563EB33 !important;
}
.stButton > button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px #2563EB55 !important;
  background: var(--accent-2) !important;
}
.stButton > button[kind="secondary"] {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  box-shadow: none !important;
  color: var(--text-2) !important;
}

/* ── Dataframe / table ────────────────────────────────────────────────── */
.stDataFrame {
  border-radius: var(--radius) !important;
  overflow: hidden !important;
  border: 1px solid var(--border) !important;
}
.stDataFrame table {
  background: var(--surface-2) !important;
}
.stDataFrame thead th {
  background: var(--surface-3) !important;
  color: var(--text-2) !important;
  font-family: var(--font-display) !important;
  font-size: 0.75rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.07em !important;
}
.stDataFrame tbody td { color: var(--text-1) !important; }
.stDataFrame tbody tr:hover td { background: var(--surface-3) !important; }

/* ── File uploader ────────────────────────────────────────────────────── */
.stFileUploader {
  background: var(--surface-2) !important;
  border: 1.5px dashed var(--border) !important;
  border-radius: var(--radius-lg) !important;
  transition: border-color .2s !important;
}
.stFileUploader:hover {
  border-color: var(--accent) !important;
}

/* ── Metrics ──────────────────────────────────────────────────────────── */
[data-testid="stMetricValue"] {
  font-family: var(--font-display) !important;
  font-size: 2rem !important;
  font-weight: 700 !important;
  color: var(--text-1) !important;
}
[data-testid="stMetricLabel"] {
  font-family: var(--font-display) !important;
  font-size: 0.72rem !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
  color: var(--text-3) !important;
}
[data-testid="stMetricDelta"] { font-family: var(--font-mono) !important; }

/* ── Radio pills in sidebar ───────────────────────────────────────────── */
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
  gap: 0.3rem !important;
  display: flex !important;
  flex-direction: column !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
  padding: 0.65rem 1rem !important;
  border-radius: 10px !important;
  border: 1px solid transparent !important;
  cursor: pointer !important;
  transition: all .18s !important;
  color: var(--text-2) !important;
  font-size: 0.88rem !important;
  font-family: var(--font-body) !important;
  background: transparent !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
  background: #1E2F4D !important;
  border-color: var(--border) !important;
  color: var(--text-1) !important;
}

/* ── Toast / alert ────────────────────────────────────────────────────── */
.stAlert {
  background: var(--surface-2) !important;
  border-radius: var(--radius) !important;
  border: 1px solid var(--border) !important;
}

/* ── Tab bar ──────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface-2) !important;
  border-radius: var(--radius) !important;
  gap: 4px !important;
  padding: 4px !important;
  border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: 8px !important;
  color: var(--text-2) !important;
  font-family: var(--font-display) !important;
  font-size: 0.84rem !important;
  font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
  background: var(--accent) !important;
  color: #fff !important;
}

/* ── Progress bar ─────────────────────────────────────────────────────── */
.stProgress > div > div { background: var(--accent) !important; }
.stProgress > div { background: var(--surface-3) !important; }

/* ── JSON viewer ──────────────────────────────────────────────────────── */
.stJson {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
}

/* ── Scrollbar ────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }

/* ── Custom components ────────────────────────────────────────────────── */
.ag-hero {
  background: linear-gradient(135deg, #0D1527 0%, #0A1628 60%, #071020 100%);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 2.5rem 3rem;
  position: relative;
  overflow: hidden;
  margin-bottom: 2rem;
}
.ag-hero::before {
  content: '';
  position: absolute;
  top: -80px; right: -80px;
  width: 320px; height: 320px;
  background: radial-gradient(circle, #2563EB18 0%, transparent 70%);
  pointer-events: none;
}
.ag-hero-eyebrow {
  font-family: var(--font-display);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--accent-2);
  margin-bottom: 0.75rem;
}
.ag-hero-title {
  font-family: var(--font-display);
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--text-1);
  line-height: 1.15;
  letter-spacing: -0.03em;
  margin: 0 0 0.6rem 0;
}
.ag-hero-sub {
  font-family: var(--font-body);
  font-size: 1rem;
  color: var(--text-2);
  line-height: 1.6;
  max-width: 560px;
  margin: 0;
}
.ag-status-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.8rem;
  border-radius: 999px;
  font-family: var(--font-display);
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.03em;
  margin-top: 1.2rem;
}
.ag-status-pill.live {
  background: #10B98115;
  border: 1px solid #10B98140;
  color: #10B981;
}
.ag-status-pill.demo {
  background: #F59E0B15;
  border: 1px solid #F59E0B40;
  color: #F59E0B;
}
.ag-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.6rem 1.8rem;
  margin-bottom: 1.2rem;
  position: relative;
}
.ag-card-title {
  font-family: var(--font-display);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-3);
  margin-bottom: 1rem;
}
.ag-divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 1.4rem 0;
}
.ag-result-yes {
  background: #10B98112;
  border: 1px solid #10B98133;
  border-radius: var(--radius);
  padding: 1.4rem 1.6rem;
}
.ag-result-no {
  background: #EF444412;
  border: 1px solid #EF444433;
  border-radius: var(--radius);
  padding: 1.4rem 1.6rem;
}
.ag-result-inconclusive {
  background: #F59E0B12;
  border: 1px solid #F59E0B33;
  border-radius: var(--radius);
  padding: 1.4rem 1.6rem;
}
.ag-result-noface {
  background: #64748B12;
  border: 1px solid #64748B33;
  border-radius: var(--radius);
  padding: 1.4rem 1.6rem;
}
.ag-verdict-label {
  font-family: var(--font-display);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin-bottom: 0.3rem;
}
.ag-verdict-label.yes { color: #10B981; }
.ag-verdict-label.no  { color: #EF4444; }
.ag-verdict-label.inc { color: #F59E0B; }
.ag-verdict-label.err { color: #64748B; }
.ag-verdict-text {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -0.02em;
}
.ag-conf-bar-wrap {
  margin-top: 0.8rem;
}
.ag-conf-label {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  color: var(--text-3);
  margin-bottom: 0.3rem;
}
.ag-payload-box {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem 1.2rem;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: #93C5FD;
  white-space: pre;
  overflow-x: auto;
}
.ag-flow-wrap {
  display: flex;
  align-items: center;
  gap: 0;
  overflow-x: auto;
  padding: 1rem 0;
}
.ag-flow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 100px;
}
.ag-flow-icon {
  width: 48px;
  height: 48px;
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}
.ag-flow-icon.accent {
  background: var(--accent-glow);
  border-color: var(--accent);
}
.ag-flow-label {
  font-family: var(--font-display);
  font-size: 0.7rem;
  font-weight: 600;
  color: var(--text-3);
  text-align: center;
  letter-spacing: 0.04em;
}
.ag-flow-arrow {
  color: var(--border);
  font-size: 1.3rem;
  padding: 0 0.3rem;
  margin-bottom: 1.3rem;
  flex-shrink: 0;
}
.ag-flow-split {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.ag-flow-branch {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.45rem 0.9rem;
  border-radius: 8px;
  font-family: var(--font-display);
  font-size: 0.78rem;
  font-weight: 600;
}
.ag-flow-branch.pub {
  background: #10B98115;
  border: 1px solid #10B98140;
  color: #10B981;
}
.ag-flow-branch.adm {
  background: #F59E0B15;
  border: 1px solid #F59E0B40;
  color: #F59E0B;
}
.ag-log-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.8rem 1rem;
  border-radius: 10px;
  border: 1px solid var(--border);
  margin-bottom: 0.5rem;
  background: var(--surface-2);
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--text-2);
}
.ag-sidebar-logo {
  padding: 1.6rem 1.4rem 1.2rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 1rem;
}
.ag-sidebar-logo-mark {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-1) !important;
  letter-spacing: -0.02em;
}
.ag-sidebar-logo-sub {
  font-family: var(--font-body);
  font-size: 0.72rem;
  color: var(--text-3) !important;
  margin-top: 0.15rem;
}
.ag-section-head {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -0.02em;
  margin-bottom: 0.3rem;
}
.ag-section-sub {
  font-family: var(--font-body);
  font-size: 0.9rem;
  color: var(--text-2);
  line-height: 1.6;
  margin-bottom: 1.6rem;
}
.ag-checklist-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 0.7rem 0;
  border-bottom: 1px solid var(--border);
}
.ag-checklist-item:last-child { border-bottom: none; }
.ag-check-icon {
  width: 20px; height: 20px;
  background: #10B98120;
  border: 1px solid #10B98150;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.65rem;
  color: #10B981;
  flex-shrink: 0;
  margin-top: 2px;
}
.ag-check-text {
  font-family: var(--font-body);
  font-size: 0.87rem;
  color: var(--text-2);
  line-height: 1.5;
}
.ag-tag {
  display: inline-block;
  padding: 0.18rem 0.55rem;
  border-radius: 6px;
  font-family: var(--font-display);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-left: 0.4rem;
}
.ag-tag-stretch {
  background: #2563EB18;
  border: 1px solid #2563EB40;
  color: #60A5FA;
}
.ag-tag-core {
  background: #10B98118;
  border: 1px solid #10B98140;
  color: #10B981;
}
.ag-limitation-item {
  padding: 1rem 1.2rem;
  border-left: 3px solid var(--border);
  margin-bottom: 0.75rem;
  border-radius: 0 var(--radius) var(--radius) 0;
  background: var(--surface-2);
}
.ag-limitation-title {
  font-family: var(--font-display);
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-1);
  margin-bottom: 0.3rem;
  letter-spacing: -0.01em;
}
.ag-limitation-body {
  font-family: var(--font-body);
  font-size: 0.83rem;
  color: var(--text-2);
  line-height: 1.55;
}
.ag-shield-ring {
  position: absolute;
  top: 1.2rem; right: 2rem;
  opacity: 0.12;
  pointer-events: none;
}
"""

st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MODEL LAYER
# ─────────────────────────────────────────────────────────────────────────────
MODEL_STD_ERROR = 6.0

try:
    from deepface import DeepFace
    DEEPFACE_OK = True
except Exception:
    DEEPFACE_OK = False


@st.cache_resource(show_spinner=False)
def load_detector():
    return cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )


def pil_to_bgr(pil_img):
    return cv2.cvtColor(np.array(pil_img.convert("RGB")), cv2.COLOR_RGB2BGR)


def detect_largest_face(bgr):
    det = load_detector()
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    faces = det.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
    if len(faces) == 0:
        return None
    return tuple(sorted(faces, key=lambda f: f[2] * f[3], reverse=True)[0])


def estimate_age(bgr):
    """Returns (age_float | None, method_str, bbox | None)."""
    bbox = detect_largest_face(bgr)
    if bbox is None:
        return None, "no_face", None
    x, y, w, h = bbox
    if DEEPFACE_OK:
        try:
            crop = bgr[y:y+h, x:x+w]
            res = DeepFace.analyze(crop, actions=["age"], enforce_detection=False, silent=True)
            if isinstance(res, list):
                res = res[0]
            return float(res["age"]), "DeepFace (pretrained)", bbox
        except Exception:
            pass
    # ── Deterministic demo heuristic (not a real age estimator) ──────────
    region = cv2.cvtColor(bgr[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
    seed = int(np.mean(region)) * 3 + int(np.std(region)) * 7
    age = 16.0 + (seed % 62)
    return age, "demo_heuristic", bbox


def confidence(age, threshold):
    gap = abs(age - threshold)
    return float(np.clip(1 - np.exp(-gap / MODEL_STD_ERROR), 0.04, 0.98))


def decide(age, threshold, margin):
    diff = age - threshold
    if abs(diff) <= margin:
        return "inconclusive"
    return "yes" if diff > 0 else "no"


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "activity_log": [],       # threshold decisions only — never raw age
        "admin_log": [],          # raw age — local demo only
        "last_bgr": None,
        "last_age": None,
        "last_method": None,
        "last_bbox": None,
        "admin_result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div class="ag-sidebar-logo">
          <div class="ag-sidebar-logo-mark">🛡&nbsp; AgeGuard</div>
          <div class="ag-sidebar-logo-sub">Boolean Privacy Platform</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Age Check",
            "Admin Console",
            "Batch Evaluation",
            "Activity Log",
            "Report",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#1E2F4D;margin:1rem 0'>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="padding:0 0.2rem">
          <div style="font-family:var(--font-display);font-size:0.68rem;font-weight:700;
                      letter-spacing:0.12em;text-transform:uppercase;color:#5B6E99;
                      margin-bottom:0.8rem">System Status</div>
          <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem">
            <div style="width:7px;height:7px;border-radius:50%;background:#10B981"></div>
            <span style="font-family:var(--font-mono);font-size:0.75rem;color:#94A3C8">
              Face Detector: OpenCV</span>
          </div>
          <div style="display:flex;align-items:center;gap:0.5rem">
            <div style="width:7px;height:7px;border-radius:50%;
                        background:{'#10B981' if DEEPFACE_OK else '#F59E0B'}"></div>
            <span style="font-family:var(--font-mono);font-size:0.75rem;color:#94A3C8">
              Age Model: {'DeepFace ✓' if DEEPFACE_OK else 'Demo Mode'}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr style='border-color:#1E2F4D;margin:1rem 0'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="padding:0 0.2rem;font-family:var(--font-body);font-size:0.75rem;
                    color:#5B6E99;line-height:1.6">
          This system is a <strong style="color:#94A3C8">learning demo</strong>.
          Not for production age verification without proper compliance review.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# HERO COMPONENT
# ─────────────────────────────────────────────────────────────────────────────
def render_hero(title, sub, eyebrow="AgeGuard Platform"):
    mode_class = "live" if DEEPFACE_OK else "demo"
    mode_text  = "● Pretrained Model Active" if DEEPFACE_OK else "● Demo Mode — Install DeepFace for live inference"
    st.markdown(
        f"""
        <div class="ag-hero">
          <svg class="ag-shield-ring" width="260" height="260" viewBox="0 0 260 260">
            <circle cx="130" cy="130" r="120" fill="none" stroke="#2563EB" stroke-width="1"/>
            <circle cx="130" cy="130" r="90"  fill="none" stroke="#2563EB" stroke-width="0.6"/>
            <circle cx="130" cy="130" r="60"  fill="none" stroke="#2563EB" stroke-width="0.4"/>
          </svg>
          <div class="ag-hero-eyebrow">{eyebrow}</div>
          <h1 class="ag-hero-title">{title}</h1>
          <p class="ag-hero-sub">{sub}</p>
          <div class="ag-status-pill {mode_class}">{mode_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def ag_card_open(label=""):
    head = f'<div class="ag-card-title">{label}</div>' if label else ""
    st.markdown(f'<div class="ag-card">{head}', unsafe_allow_html=True)

def ag_card_close():
    st.markdown('</div>', unsafe_allow_html=True)

def hr():
    st.markdown('<hr class="ag-divider">', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE ① — OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
if page == "Overview":
    render_hero(
        "Privacy Through\nBoolean Design",
        "AgeGuard verifies age with a yes / no answer. Callers never see the estimated age — "
        "only a threshold decision and a confidence score. Internal engineers retain access to "
        "the raw model output for evaluation.",
    )

    # ── Architecture flow ───────────────────────────────────────────────────
    ag_card_open("Architecture — how data flows")
    st.markdown(
        """
        <div class="ag-flow-wrap">
          <div class="ag-flow-step">
            <div class="ag-flow-icon">📷</div>
            <div class="ag-flow-label">Image<br>Upload</div>
          </div>
          <div class="ag-flow-arrow">→</div>
          <div class="ag-flow-step">
            <div class="ag-flow-icon">🧑</div>
            <div class="ag-flow-label">Face<br>Detection</div>
          </div>
          <div class="ag-flow-arrow">→</div>
          <div class="ag-flow-step">
            <div class="ag-flow-icon accent">📈</div>
            <div class="ag-flow-label">Age<br>Estimation</div>
          </div>
          <div class="ag-flow-arrow">→</div>
          <div class="ag-flow-step">
            <div class="ag-flow-icon">⚖️</div>
            <div class="ag-flow-label">Threshold<br>Decision</div>
          </div>
          <div class="ag-flow-arrow">→</div>
          <div class="ag-flow-split">
            <div class="ag-flow-branch pub">✅&nbsp; Public API — YES / NO / INCONCLUSIVE</div>
            <div class="ag-flow-branch adm">🔐&nbsp; Admin Console — raw age (local demo only)</div>
          </div>
        </div>
        <div style="font-family:var(--font-body);font-size:0.8rem;color:#5B6E99;margin-top:0.5rem">
          The raw age estimate never leaves the model layer toward normal callers.
          Only the boolean result and confidence cross the public API boundary.
        </div>
        """,
        unsafe_allow_html=True,
    )
    ag_card_close()

    # ── Two endpoint comparison ─────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        ag_card_open("POST /check_age — public endpoint")
        st.markdown(
            """
            <div style="font-family:var(--font-body);font-size:0.87rem;color:#94A3C8;
                        line-height:1.65;margin-bottom:1rem">
              Accepts an image + one or more age thresholds.<br>
              Returns per-threshold:
            </div>
            """,
            unsafe_allow_html=True,
        )
        fields = [
            ("is_above_threshold", "bool | null", "The core boolean — true / false / null (inconclusive)"),
            ("confidence",          "float 0–1",  "How certain the model is, given its error margin"),
            ("decision",            "string",      "yes · no · inconclusive"),
        ]
        for f, t, d in fields:
            st.markdown(
                f"""<div style="padding:0.5rem 0;border-bottom:1px solid #1E2F4D">
                  <span style="font-family:var(--font-mono);font-size:0.8rem;color:#60A5FA">{f}</span>
                  <span style="font-family:var(--font-mono);font-size:0.72rem;color:#5B6E99;margin-left:0.5rem">{t}</span>
                  <div style="font-family:var(--font-body);font-size:0.78rem;color:#5B6E99;margin-top:0.2rem">{d}</div>
                </div>""",
                unsafe_allow_html=True,
            )
        st.markdown(
            '<div style="margin-top:0.9rem;font-family:var(--font-body);font-size:0.8rem;'
            'color:#10B981">✓ The exact estimated age is absent from this response.</div>',
            unsafe_allow_html=True,
        )
        ag_card_close()

    with c2:
        ag_card_open("POST /admin/estimate_age_raw — internal only")
        st.markdown(
            """
            <div style="font-family:var(--font-body);font-size:0.87rem;color:#94A3C8;
                        line-height:1.65;margin-bottom:1rem">
              Password-gated, local-demo-only endpoint. Exposes the raw estimated age
              so ML engineers can sanity-check and benchmark the model.
            </div>
            """,
            unsafe_allow_html=True,
        )
        adm_fields = [
            ("estimated_age",    "float",  "Raw model output in years"),
            ("model_used",       "string", "DeepFace · demo_heuristic · etc."),
            ("error_band_years", "float",  "Approximate ±1σ error of this model"),
            ("bbox",             "object", "Face bounding box for visual inspection"),
        ]
        for f, t, d in adm_fields:
            st.markdown(
                f"""<div style="padding:0.5rem 0;border-bottom:1px solid #1E2F4D">
                  <span style="font-family:var(--font-mono);font-size:0.8rem;color:#FBBF24">{f}</span>
                  <span style="font-family:var(--font-mono);font-size:0.72rem;color:#5B6E99;margin-left:0.5rem">{t}</span>
                  <div style="font-family:var(--font-body);font-size:0.78rem;color:#5B6E99;margin-top:0.2rem">{d}</div>
                </div>""",
                unsafe_allow_html=True,
            )
        st.markdown(
            '<div style="margin-top:0.9rem;font-family:var(--font-body);font-size:0.8rem;'
            'color:#F59E0B">⚠ Never exposed in production deployments.</div>',
            unsafe_allow_html=True,
        )
        ag_card_close()

    # ── Project checklist ───────────────────────────────────────────────────
    ag_card_open("Project acceptance criteria")
    items = [
        ("Normal endpoint never returns exact age", "core"),
        ("Thresholds 18, 21 and 60 all supported", "core"),
        ("Custom threshold input for any value", "core"),
        ("Inconclusive zone when estimate is too close to the threshold", "stretch"),
        ("Multiple boolean checks (thresholds) in a single request", "stretch"),
        ("Activity log stores only threshold decisions — never raw age", "core"),
        ("Admin / internal view exposes raw estimated age (local demo only)", "core"),
        ("Batch evaluation across 20–30 images with MAE & accuracy reporting", "core"),
        ("Per-group bias check (lighting / age bands) in batch view", "stretch"),
        ("Limitations report covering known weaknesses of age estimation", "core"),
        ("Demo clearly shows why yes/no is safer than returning full age", "core"),
    ]
    for text, kind in items:
        tag = (
            '<span class="ag-tag ag-tag-core">core</span>'
            if kind == "core"
            else '<span class="ag-tag ag-tag-stretch">stretch</span>'
        )
        st.markdown(
            f"""<div class="ag-checklist-item">
              <div class="ag-check-icon">✓</div>
              <div class="ag-check-text">{text}{tag}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    ag_card_close()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE ② — AGE CHECK  (public endpoint)
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Age Check":
    render_hero(
        "Public Age Check",
        "Upload a photo and select thresholds. The platform returns only a boolean verdict "
        "and confidence per threshold — the raw estimated age is never disclosed.",
        eyebrow="POST /check_age",
    )

    # ── Controls ─────────────────────────────────────────────────────────────
    ag_card_open("Request parameters")
    up_col, param_col = st.columns([1, 1.4])

    with up_col:
        uploaded = st.file_uploader(
            "Image", type=["jpg", "jpeg", "png"],
            label_visibility="visible",
            help="One face per image gives the best result.",
        )
        if uploaded:
            st.image(
                Image.open(uploaded),
                use_container_width=True,
                caption="Uploaded image",
            )

    with param_col:
        selected_thresholds = st.multiselect(
            "Select Threshold(s)",
            options=[18, 21, 60],
            default=[18],
            help="You can select one or more thresholds."
        )

        custom = st.number_input(
            "Custom Threshold (0 = none)",
            min_value=0,
            max_value=120,
            value=0,
            step=1,
        )

        if custom > 0:
            if custom not in selected_thresholds:
                selected_thresholds.append(custom)

        st.markdown(
            "<div style='font-family:var(--font-display);font-size:0.72rem;"
            "font-weight:600;letter-spacing:0.1em;text-transform:uppercase;"
            "color:#5B6E99;margin-bottom:0.5rem'>Selected Threshold</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <span style="
                display:inline-block;
                padding:0.25rem 0.65rem;
                border-radius:999px;
                background:#2563EB18;
                border:1px solid #2563EB40;
                font-family:var(--font-display);
                font-size:0.78rem;
                font-weight:600;
                color:#60A5FA;">
                {", ".join(f"{t}+" for t in selected_thresholds)}
            </span>
            """,
            unsafe_allow_html=True,
        )
    ag_card_close()

    run = st.button(
        "Run Age Check  →",
        disabled=(uploaded is None),
        type="primary",
    )

    if run and uploaded:
        bgr = pil_to_bgr(Image.open(uploaded))
        
        with st.spinner("Analysing face…"):

            files = {
                "image": (
                    uploaded.name,
                    uploaded.getvalue(),
                    uploaded.type
                )
            }

            data = {
            "user_id": "demo_user",
            "thresholds": ",".join(map(str, selected_thresholds))
            }

            headers = {
                "Authorization": f"Bearer {API_TOKEN}"
            }
            
            response = requests.post(
                API_URL,
                files=files,
                data=data,
                headers=headers
            ) 

            if response.status_code != 200:
                st.error(f"API Error: {response.text}")
                st.stop()

            result = response.json()

            st.session_state.api_result = result

            # Save information for Admin Console
            st.session_state.admin_result = {
                "thresholds": selected_thresholds,
                "results": result["results"],
                "latency_ms": result["latency_ms"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            st.session_state.last_bgr = bgr.copy()
            st.session_state.last_age = None
            st.session_state.last_method = "DeepFace"
            st.session_state.last_bbox = None

        if result is None:
            st.markdown(
                '<div class="ag-result-noface">'
                '<div class="ag-verdict-label err">Result</div>'
                '<div class="ag-verdict-text">No face detected</div>'
                '<div style="font-family:var(--font-body);font-size:0.83rem;'
                'color:#94A3C8;margin-top:0.5rem">'
                'Please upload a clear, front-facing photograph.</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            st.session_state.activity_log.append({
                "ts": datetime.now().isoformat(timespec="seconds"),
                "threshold": selected_thresholds,
                "results": "no_face",
            })
        else:

            results = result["results"]

            cols = st.columns(len(results))
            results_for_log = {}

            for col, (threshold_label, value) in zip(cols, results.items()):

                decision = value["decision"]
                confidence = value["confidence"]
                is_above = value["is_above_threshold"]

                # Convert backend decision to UI decision
                if decision == "pass":
                    d = "yes"
                elif decision == "fail":
                    d = "no"
                else:
                    d = "inconclusive"

                c = confidence
                results_for_log[threshold_label] = {
                    "decision": decision,
                    "confidence": round(confidence, 3),
                    "is_above_threshold": is_above
                }
                css_map = {
                    "yes": "ag-result-yes",
                    "no": "ag-result-no",
                    "inconclusive": "ag-result-inconclusive"
                }

                lbl_map = {
                    "yes": "yes",
                    "no": "no",
                    "inconclusive": "inc"
                }

                icon = {
                    "yes": "✅",
                    "no": "❌",
                    "inconclusive": "❓"
                }

                txt = {
                    "yes": "Above Threshold",
                    "no": "Below Threshold",
                    "inconclusive": "Inconclusive"
                }

                if is_above is None:
                    bool_v = "null"
                else:
                    bool_v = str(is_above).lower()
                
                with col:
                    st.markdown(
                        f"""<div class="{css_map[d]}" style="text-align:center">
                          <div class="ag-verdict-label {lbl_map[d]}">Threshold {threshold_label}</div>
                          <div style="font-size:2.2rem;margin:0.4rem 0">{icon[d]}</div>
                          <div class="ag-verdict-text">{txt[d]}</div>
                          <div style="font-family:var(--font-mono);font-size:0.8rem;
                                      color:#94A3C8;margin-top:0.5rem">
                            is_above_threshold: <strong style="color:#F0F6FF">{bool_v}</strong>
                          </div>
                        </div>""",
                        unsafe_allow_html=True,
                    )
                    st.progress(c)
                    st.markdown(
                        f"<div style='font-family:var(--font-mono);font-size:0.72rem;"
                        f"color:#5B6E99;text-align:center'>confidence: {c:.0%}</div>",
                        unsafe_allow_html=True,
                    )


            hr()

            ag_card_open("API response payload — sent to normal callers")

            import json

            st.code(
                json.dumps(result, indent=4),
                language="json"
            )

            st.markdown(
                "<div style='font-family:var(--font-body);font-size:0.8rem;"
                "color:#10B981;margin-top:0.6rem'>"
                "✓ No <code>estimated_age</code> field anywhere in this response.</div>",
                unsafe_allow_html=True,
            )

            ag_card_close()

            st.session_state.activity_log.append({
                "ts": datetime.now().isoformat(timespec="seconds"),
                "threshold": selected_thresholds,
                "results": results_for_log,
            }) 


# ─────────────────────────────────────────────────────────────────────────────
# PAGE ③ — ADMIN CONSOLE
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Admin Console":
    render_hero(
        "Admin Console",
        "Password-gated internal view. Exposes the raw estimated age for model evaluation. "
        "This endpoint must never be reachable by normal platform callers.",
        eyebrow="POST /admin/estimate_age_raw — local demo only",
    )

    ag_card_open("Authentication")
    pwd = st.text_input(
        "Admin Password",
        type="password",
        placeholder="Enter password to unlock  (demo: admin123)",
    )
    ag_card_close()

    authed = pwd == "admin123"

    if pwd and not authed:
        st.markdown(
            "<div style='color:#EF4444;font-family:var(--font-display);"
            "font-size:0.85rem;padding:0.5rem 0'>✗ Incorrect password</div>",
            unsafe_allow_html=True,
        )

    if authed:
        st.markdown(
            "<div style='color:#10B981;font-family:var(--font-display);"
            "font-size:0.85rem;padding:0.5rem 0 1.2rem'>✓ Authenticated — internal view unlocked</div>",
            unsafe_allow_html=True,
        )
        headers = {
            "Authorization": f"Bearer {API_TOKEN}"
        }

        response = requests.get(
            "http://127.0.0.1:8000/admin/latest",
            headers=headers
        )
        if response.status_code == 200:
          admin_data = response.json()
        else:
            st.info("No Age Check has been performed yet.")
            admin_data = None
        if admin_data:
            ag_card_open("Dashboard Summary")

            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric(
                    "Thresholds",
                    ", ".join(f"{t}+" for t in admin_data["thresholds"])
                )

            with m2:
                st.metric(
                    "Estimated Age",
                    f"{admin_data['estimated_age']} yrs"
                )

            with m3:
                st.metric(
                    "Latency",
                    f"{admin_data['latency_ms']} ms"
                )

            ag_card_close()

            hr()
            ag_card_open("Latest Processed Age Check")
            left_col, right_col = st.columns([1, 1.3])
            with left_col:

                if st.session_state.last_bgr is not None:
                    st.image(
                        cv2.cvtColor(
                            st.session_state.last_bgr,
                            cv2.COLOR_BGR2RGB
                        ),
                        use_container_width=True,
                        caption="Last uploaded image"
                    )

            with right_col:

                col1, col2 = st.columns(2)
              
            with col1:
                st.metric(
                    "Estimated Age",
                    f"{admin_data['estimated_age']} years"
                )

                st.metric(
                    "Thresholds",
                    ", ".join(f"{t}+" for t in admin_data["thresholds"])
                )

                st.write("### Results")

                for threshold, value in admin_data["results"].items():
                    st.write(
                        f"**{threshold}** → "
                        f"{value['decision'].upper()} "
                        f"({value['confidence']:.0%})"
                    )

            with col2:
    
                st.metric(
                    "Latency",
                    f"{admin_data['latency_ms']} ms"
                )

                st.metric(
                    "Model",
                    admin_data["model_used"]
                )

            st.caption(f"Processed at: {admin_data['timestamp']}")

            ag_card_close()    
        # Privacy comparison callout
        ag_card_open("Why boolean output is safer")
        reasons = [
            ("Data minimisation", "The API returns only what the caller needs. A boolean gate does not reveal the person's age."),
            ("Reduced re-identification risk", "An exact age combined with other signals can re-identify a person. A yes/no verdict cannot."),
            ("Smaller breach surface", "If logs or API responses leak, a list of yes/no decisions is far less sensitive than a list of estimated ages."),
            ("Simpler compliance story", "Storing less personal data reduces the scope of privacy reviews, even without formal compliance claims."),
        ]
        for title, body in reasons:
            st.markdown(
                f"""<div style="padding:0.7rem 0;border-bottom:1px solid #1E2F4D">
                  <div style="font-family:var(--font-display);font-size:0.85rem;
                              font-weight:600;color:#F0F6FF;margin-bottom:0.2rem">
                    → {title}</div>
                  <div style="font-family:var(--font-body);font-size:0.82rem;
                              color:#94A3C8;line-height:1.55">{body}</div>
                </div>""",
                unsafe_allow_html=True,
            )
        ag_card_close()


# ─────────────────────────────────────────────────────────────────────────────
# PAGE ④ — BATCH EVALUATION
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Batch Evaluation":
    render_hero(
        "Batch Evaluation",
        "Upload 20–30 labelled images to measure the model's Mean Absolute Error and "
        "threshold accuracy at 18, 21, and 60. Optionally tag images by group to surface bias.",
        eyebrow="Week 3 deliverable — MAE & accuracy report",
    )

    ag_card_open("Upload & label test images")
    files = st.file_uploader(
        "Images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Upload 20–30 images with approximately known ages.",
    )
    ag_card_close()

    if files:
        ag_card_open("Ground-truth labels")
        st.markdown(
            "<div style='font-family:var(--font-body);font-size:0.83rem;color:#5B6E99;"
            "margin-bottom:0.8rem'>Enter the approximate known age and an optional "
            "group label (e.g. lighting condition or age band) for each image.</div>",
            unsafe_allow_html=True,
        )
        label_df = pd.DataFrame({
            "filename": [f.name for f in files],
            "true_age": [25] * len(files),
            "group":    ["default"] * len(files),
        })
        edited = st.data_editor(label_df, num_rows="fixed", use_container_width=True, hide_index=True)
        ag_card_close()

        if st.button("▶  Run Batch Evaluation", type="primary"):
            rows = []
            prog = st.progress(0.0, text="Analysing images…")
            for i, (f, (_, row)) in enumerate(zip(files, edited.iterrows())):
                bgr = pil_to_bgr(Image.open(f))
                age, method, _ = estimate_age(bgr)
                ta = float(row["true_age"])
                
                rows.append({
                    "Filename":   row["filename"],
                    "Group":      row["group"],
                    "True Age":   ta,
                    "Est. Age":   round(age, 1) if age else None,
                    "Abs. Error": round(abs(age - ta), 1) if age else None,
                    "Method":     method,
                    "above_18":   age >= 18 if age else None,
                    "above_21":   age >= 21 if age else None,
                    "above_60":   age >= 60 if age else None,
                    "true_18":    ta >= 18,
                    "true_21":    ta >= 21,
                    "true_60":    ta >= 60,
                })
                
                prog.progress((i + 1) / len(files), text=f"Analysed {i+1}/{len(files)}")
            prog.empty()

            res = pd.DataFrame(rows)
            valid = res.dropna(subset=["Abs. Error"])

            # ── Summary metrics ─────────────────────────────────────────────
            if not valid.empty:
                ag_card_open("Summary")
                mae = valid["Abs. Error"].mean()
                m0, m1, m2, m3 = st.columns(4)
                m0.metric("Images evaluated", f"{len(valid)}/{len(res)}")
                m1.metric("MAE (years)", f"{mae:.2f}")
                for col, t in zip([m2, m3], [18, 21]):
                    acc = (valid[f"above_{t}"] == valid[f"true_{t}"]).mean()
                    col.metric(f"Accuracy @ {t}+", f"{acc:.0%}")
                _, m4, m5, _ = st.columns(4)
                acc60 = (valid["above_60"] == valid["true_60"]).mean()
                m4.metric("Accuracy @ 60+", f"{acc60:.0%}")
                m5.metric("Face detect rate", f"{len(valid)/len(res):.0%}")
                ag_card_close()

                tabs = st.tabs(["Per-image results", "Error distribution", "Bias by group"])
                with tabs[0]:
                    display_cols = ["Filename", "Group", "True Age", "Est. Age", "Abs. Error", "Method"]
                    st.dataframe(res[display_cols], use_container_width=True, hide_index=True)

                with tabs[1]:
                    st.bar_chart(
                        valid.set_index("Filename")["Abs. Error"],
                        height=260,
                        color="#2563EB",
                    )

                with tabs[2]:
                    if valid["Group"].nunique() > 1:
                        bias = valid.groupby("Group")["Abs. Error"].mean().reset_index()
                        bias.columns = ["Group", "Mean Abs. Error"]
                        st.bar_chart(bias.set_index("Group"), height=240, color="#F59E0B")
                    else:
                        st.info("Add different group labels to compare MAE across subgroups.")
            else:
                st.warning("No faces were detected in any uploaded image. Try clearer, front-facing photos.")
    else:
        st.info("Upload at least one image to begin evaluation.")


# ─────────────────────────────────────────────────────────────────────────────
# PAGE ⑤ — ACTIVITY LOG
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Activity Log":
    render_hero(
        "Activity Log",
        "Every age-check call appends a structured entry here. Only threshold decisions and "
        "confidence scores are recorded — the raw estimated age is never written to this log.",
        eyebrow="Privacy-preserving audit trail",
    )

    ag_card_open("Design principle")
    st.markdown(
        """
        <div style="display:flex;gap:2rem;flex-wrap:wrap">
          <div style="flex:1;min-width:200px">
            <div style="font-family:var(--font-display);font-size:0.72rem;font-weight:700;
                        letter-spacing:0.1em;text-transform:uppercase;color:#10B981;
                        margin-bottom:0.4rem">✓ What IS stored</div>
            <div style="font-family:var(--font-mono);font-size:0.8rem;color:#94A3C8;line-height:1.8">
              timestamp<br>threshold(s) checked<br>decision (yes / no / inconclusive)<br>confidence score
            </div>
          </div>
          <div style="flex:1;min-width:200px">
            <div style="font-family:var(--font-display);font-size:0.72rem;font-weight:700;
                        letter-spacing:0.1em;text-transform:uppercase;color:#EF4444;
                        margin-bottom:0.4rem">✗ What is NEVER stored</div>
            <div style="font-family:var(--font-mono);font-size:0.8rem;color:#94A3C8;line-height:1.8">
              raw estimated age<br>face image or crop<br>bounding box coordinates<br>model internal scores
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    ag_card_close()

    log = st.session_state.activity_log
    if log:
        rows = []
        for entry in log:
            if entry["results"] == "no_face":
                rows.append({"Timestamp": entry["ts"], "Threshold": str(entry["threshold"]),
                              "Result": "no_face", "Confidence": "—"})
            else:
                for t, v in entry["results"].items():
                    rows.append({
                        "Timestamp": entry["ts"],
                        "Threshold": f"{t}+",
                        "Decision":  v["decision"],
                        "Confidence": f"{v['confidence']:.0%}",
                    })
        log_df = pd.DataFrame(rows)
        st.dataframe(log_df, use_container_width=True, hide_index=True)

        buf = io.StringIO()
        log_df.to_csv(buf, index=False)
        dl_col, clr_col, _ = st.columns([1, 1, 3])
        with dl_col:
            st.download_button(
                "⬇  Download CSV",
                buf.getvalue(),
                file_name="ageguard_activity_log.csv",
                mime="text/csv",
            )
        with clr_col:
            if st.button("Clear log", type="secondary"):
                st.session_state.activity_log = []
                st.rerun()
    else:
        st.markdown(
            "<div style='font-family:var(--font-body);font-size:0.9rem;color:#5B6E99;"
            "padding:2rem;text-align:center;border:1px dashed #1E2F4D;border-radius:12px'>"
            "No entries yet — run a check on the <strong style='color:#94A3C8'>Age Check</strong> "
            "page to populate the log.</div>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# PAGE ⑥ — REPORT
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Report":
    render_hero(
        "Limitations & Report",
        "An honest account of what pretrained age estimation can and cannot do, "
        "and why the boolean-privacy design pattern matters.",
        eyebrow="Week 4 deliverable",
    )

    ag_card_open("Model accuracy & error")
    limitations = [
        (
            "Mean Absolute Error of ~4–8 years",
            "Most published pretrained age estimators achieve 4–8 years MAE on standard benchmarks. "
            "This means a real teenager could be estimated in their mid-twenties, or vice versa — "
            "making hard threshold unreliable near the boundary. The inconclusive zone exists specifically "
            "to handle this uncertainty honestly."
        ),
        (
            "Single-frame noise",
            "A single photograph is one noisy sample. Lighting, angle, expression, compression "
            "artefacts, and image resolution all shift the estimate. A production system might "
            "request a higher-quality image or average across several frames when confidence is low."
        ),
        (
            "Demographic bias",
            "Pretrained models often perform inconsistently across ethnicities, genders, and age groups, "
            "particularly near the extremes of the training distribution (very young children, elderly adults). "
            "The batch evaluation page includes a group-level MAE check to surface this."
        ),
        (
            "Heavy makeup, filters & accessories",
            "Sunglasses, heavy contouring, beauty filters, and certain hairstyles can shift estimates "
            "by several years. The model has no way to flag these conditions automatically."
        ),
    ]
    for title, body in limitations:
        st.markdown(
            f"""<div class="ag-limitation-item">
              <div class="ag-limitation-title">⚠ {title}</div>
              <div class="ag-limitation-body">{body}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    ag_card_close()

    ag_card_open("Why boolean output is safer than returning age")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div style="background:#EF444408;border:1px solid #EF444430;border-radius:12px;
                        padding:1.2rem;margin-bottom:0.8rem">
              <div style="font-family:var(--font-display);font-size:0.78rem;font-weight:700;
                          letter-spacing:0.08em;text-transform:uppercase;color:#EF4444;
                          margin-bottom:0.6rem">Without boolean privacy</div>
              <div style="font-family:var(--font-mono);font-size:0.78rem;color:#94A3C8;line-height:1.8">
                estimated_age: 23.4<br>
                dob_estimate: "~2001"<br>
                confidence: 0.78
              </div>
              <div style="font-family:var(--font-body);font-size:0.78rem;color:#EF4444;margin-top:0.7rem">
                → Combines with name, device, location to create a profile.<br>
                → Log breach exposes precise personal attribute.<br>
                → Caller can build age-derivative inferences.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div style="background:#10B98108;border:1px solid #10B98130;border-radius:12px;
                        padding:1.2rem;margin-bottom:0.8rem">
              <div style="font-family:var(--font-display);font-size:0.78rem;font-weight:700;
                          letter-spacing:0.08em;text-transform:uppercase;color:#10B981;
                          margin-bottom:0.6rem">With boolean privacy</div>
              <div style="font-family:var(--font-mono);font-size:0.78rem;color:#94A3C8;line-height:1.8">
                is_above_threshold: true<br>
                confidence: 0.87<br>
                decision: "yes"
              </div>
              <div style="font-family:var(--font-body);font-size:0.78rem;color:#10B981;margin-top:0.7rem">
                → Reveals nothing about the exact age.<br>
                → Log breach exposes only a boolean value.<br>
                → Fulfils the caller's need without over-sharing.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    ag_card_close()

    ag_card_open("Scope & compliance disclaimer")
    st.markdown(
        """
        <div style="font-family:var(--font-body);font-size:0.87rem;color:#94A3C8;line-height:1.7">
        This project is a <strong style="color:#F0F6FF">learning demonstration</strong> of privacy-preserving
        API design patterns and pretrained model integration. It is <strong style="color:#EF4444">not</strong>
        a legally compliant age-verification system and should not be used as a substitute for
        identity document verification in regulated contexts (alcohol, gambling, adult content, etc.).<br><br>
        The demo heuristic fallback (used when no pretrained model is installed) has
        <strong style="color:#F0F6FF">no real predictive validity</strong> and exists solely to keep the
        user interface functional in offline / restricted environments.
        </div>
        """,
        unsafe_allow_html=True,
    )
    ag_card_close()

    ag_card_open("Week-by-week learning map")
    weeks = [
        ("Week 1", "Model Setup", "Get the age estimator running on a single image. Understand regression output vs. classification, and what a raw float age estimate means."),
        ("Week 2", "Boolean Endpoint", "Design /check_age to return only yes/no/inconclusive. Introduce the confidence score and the inconclusive margin concept."),
        ("Week 3", "Threshold Testing", "Evaluate thresholds 18, 21, and 60 across a labelled test set. Compute MAE, threshold accuracy, and a first bias check."),
        ("Week 4", "Demo & Report", "Build the Streamlit privacy comparison, write the limitations report, and communicate why boolean design improves privacy."),
    ]
    for wk, focus, desc in weeks:
        st.markdown(
            f"""<div style="display:flex;gap:1.2rem;padding:0.9rem 0;border-bottom:1px solid #1E2F4D;align-items:flex-start">
              <div style="min-width:72px;font-family:var(--font-display);font-size:0.72rem;
                          font-weight:700;letter-spacing:0.08em;text-transform:uppercase;
                          color:#2563EB;padding-top:2px">{wk}</div>
              <div>
                <div style="font-family:var(--font-display);font-size:0.9rem;font-weight:600;
                            color:#F0F6FF;margin-bottom:0.2rem">{focus}</div>
                <div style="font-family:var(--font-body);font-size:0.82rem;color:#94A3C8;line-height:1.55">{desc}</div>
              </div>
            </div>""",
            unsafe_allow_html=True,
        )
    ag_card_close()
