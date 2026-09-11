import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from fpdf import FPDF
import tempfile
import os

# --- 1. LUXURY PURPLE CLINICAL THEME ---
st.set_page_config(page_title="Genetic Risk Interrogator", page_icon="🧬", layout="wide")

st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #2c1654 0%, #4a2874 100%);
        color: white;
        padding: 30px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(44,22,84,0.1);
    }
    .main-header h1 {
        color: white;
        font-weight: 700;
        margin: 0;
        font-size: 28px;
    }
    .main-header p {
        color: #e6dbf2;
        margin-top: 5px;
        font-weight: 300;
    }
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #d4c2ed;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(74,40,116,0.03);
    }
    div[data-testid="metric-container"] > label {
        color: #4a2874 !important;
        font-weight: 600;
    }
    div[data-testid="metric-container"] > div > div {
        color: #6b35af !important;
        font-weight: 700;
    }
    section[data-testid="stSidebar"] {
        background-color: #ede5f5;
        border-right: 1px solid #d4c2ed;
    }
    
    /* Style Primary Button to Dark Purple */
    button[kind="primary"] {
        background-color: #4a2874 !important;
        border-color: #4a2874 !important;
    }
    button[kind="primary"]:hover {
        background-color: #381e5c !important;
        border-color: #381e5c !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- UI HEADER ---
st.markdown('<div class="main-header"><h1>🧬 Genetic Risk Interrogator</h1><p>Advanced Multi-Ancestry & Environmental Contextualization</p></div>', unsafe_allow_html=True)

# --- 2. PROFESSIONAL SIDEBAR & PERSONA PRESETS ---
st.sidebar.header("🎛️ Patient Intake & Personas")

persona = st.sidebar.selectbox(
    "Load Clinical Persona",
    ["Custom Input", "Patient A: Mixed West African / European", "Patient B: East Asian Urban Cohort", "Patient C: South Asian Baseline"]
)

if persona == "Patient A: Mixed West African / European":
    default_prs, default_env, d_eur, d_afr, d_eas, d_sas = 2.85, 0.9, 15.0, 75.0, 5.0, 5.0
elif persona == "Patient B: East Asian Urban Cohort":
    default_prs, default_env, d_eur, d_afr, d_eas, d_sas = 1.40, 1.3, 5.0, 5.0, 85.0, 5.0
elif persona == "Patient C: South Asian Baseline":
    default_prs, default_env, d_eur, d_afr, d_eas, d_sas = 2.10, 1.0, 10.0, 5.0, 5.0, 80.0
else:
    default_prs, default_env, d_eur, d_afr, d_eas, d_sas = 2.50, 1.0, 25.0, 25.0, 25.0, 25.0

raw_prs = st.sidebar.number_input("Raw Polygenic Risk Score (PRS)", value=default_prs)
env_factor = st.sidebar.slider(
    "Environmental Risk Multiplier",
    0.5, 2.0, default_env, step=0.05,
    help="Adjusts risk based on environmental stressors."
)

st.sidebar.markdown("---")
st.sidebar.header("🌍 Global Ancestry Admixture (%)")
st.sidebar.markdown("Input fractions summing to 100%.")

col1, col2 = st.sidebar.columns(2)
with col1:
    eur = st.sidebar.slider("European (EUR)", 0.0, 100.0, d_eur, key="eur", step=1.0)
    afr = st.sidebar.slider("African (AFR)", 0.0, 100.0, d_afr, key="afr", step=1.0)
with col2:
    eas = st.sidebar.slider("E. Asian (EAS)", 0.0, 100.0, d_eas, key="eas", step=1.0)
    sas = st.sidebar.slider("S. Asian (SAS)", 0.0, 100.0, d_sas, key="sas", step=1.0)

total = eur + afr + eas + sas
if total > 0:
    eur_f, afr_f, eas_f, sas_f = eur/total, afr/total, eas/total, sas/total
else:
    eur_f, afr_f, eas_f, sas_f = 0.25, 0.25, 0.25, 0.25

if total != 100:
    st.sidebar.warning(f"⚠️ Total Admixture is {total}%. Please adjust sliders to sum to 100%.")


# --- MAIN LAYOUT: VISUALIZATION ---
st.markdown("### 📊 Ancestry Profile Visualization")

ancestry_df = pd.DataFrame({
    'Ancestry': ['European', 'African', 'East Asian', 'South Asian'],
    'Percentage': [eur, afr, eas, sas]
})

base = alt.Chart(ancestry_df).encode(
    x=alt.X('Ancestry', sort=None, axis=alt.Axis(title='')),
    y=alt.Y('Percentage', title='Population Fraction (%)'),
    tooltip=['Ancestry', alt.Tooltip('Percentage', format='.1f')]
)

bar = base.mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6).encode(
    color=alt.Color(
        'Ancestry',
        scale=alt.Scale(
            domain=['European', 'African', 'East Asian', 'South Asian'],
            range=['#4e79a7', '#e15759', '#76b7b2', '#59a14f']
        ),
        legend=None
    ),
    opacity=alt.value(0.9)
)

text = base.mark_text(dy=-15).encode(
    text=alt.Text('Percentage', format='.1f'),
    color=alt.value('#333')
)

chart = (bar + text).properties(height=380, background="#ffffff").configure_view(
    strokeWidth=0
)
st.altair_chart(chart, use_container_width=True)


# --- 4. RISK ASSESSMENT, COMPARISON & EXPORT REPORT ---
st.markdown("<br><hr><h2>🎯 Final Diagnostic Assessment & Report</h2>", unsafe_allow_html=True)

if st.button("Run Contextual Analysis", type="primary"):
    bias_correction = 1.0 - (eur_f * 0.25)
    adj_score = round(raw_prs * bias_correction * env_factor, 3)
    recommendation = f"Adjusted for {int(eur_f*100)}% European and multi-ancestry admixture model. Mitigated false-positive risk over-attribution common in Euro-centric GWAS training sets."

    with st.spinner("Synthesizing adjusted risk..."):
        st.session_state['last_analysis'] = {
            "raw_prs": raw_prs,
            "adj_score": adj_score,
            "eur": eur,
            "afr": afr,
            "eas": eas,
            "sas": sas,
            "env": env_factor,
            "recommendation": recommendation,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with st.expander("📂 View Full Diagnostic Report & Comparison", expanded=True):
            st.markdown("#### Bias Mitigation Impact")
            comp_col1, comp_col2 = st.columns(2)
            
            with comp_col1:
                st.metric(
                    label="Uncorrected Standard PRS (Baseline Risk)",
                    value=f"{raw_prs:.3f}",
                    delta=f"{((raw_prs - adj_score)/raw_prs)*100:.1f}% potential overestimation",
                    delta_color="inverse"
                )
            with comp_col2:
                st.metric(
                    label="Context-Adjusted Risk Score",
                    value=f"{adj_score:.3f}",
                    help="Final score adjusted for population stratification and environmental multipliers."
                )
            
            st.markdown("---")
            st.markdown("#### Clinical Interpretation & Recommendations")
            st.success(recommendation)

# --- EXPORT REPORT BUTTON (PDF GENERATION) ---
if 'last_analysis' in st.session_state:
    res = st.session_state['last_analysis']
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 18)
    pdf.set_text_color(44, 22, 84)
    pdf.cell(0, 10, "Genetic Risk Interrogator - Diagnostic Report", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("helvetica", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, f"Generated on: {res['timestamp']}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)
    
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(74, 40, 116)
    pdf.cell(0, 10, "1. Patient Genomic Summary", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "", 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 7, f"- Raw Polygenic Risk Score (PRS): {res['raw_prs']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"- Environmental Risk Multiplier: {res['env']}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(74, 40, 116)
    pdf.cell(0, 10, "2. Global Admixture Breakdown", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "", 11)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 7, f"- European (EUR): {res['eur']}%", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"- African (AFR): {res['afr']}%", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"- East Asian (EAS): {res['eas']}%", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"- South Asian (SAS): {res['sas']}%", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(74, 40, 116)
    pdf.cell(0, 10, "3. Risk Evaluation Results & Recommendations", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 7, f"Context-Adjusted Risk Score: {res['adj_score']}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "", 11)
    pdf.multi_cell(0, 7, f"Clinical Interpretation: {res['recommendation']}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        tmp_path = tmp_file.name

    with open(tmp_path, "rb") as pdf_file:
        PDF_bytes = pdf_file.read()

    st.download_button(
        label="📥 Download Professional Clinical Report (PDF)",
        data=PDF_bytes,
        file_name=f"clinical_risk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf"
    )
