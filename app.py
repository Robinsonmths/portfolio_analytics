import streamlit as st

st.set_page_config(
    page_title="Robinson Matheus | Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS CUSTOMIZADO ────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #161B22;
        border: 1px solid #21262D;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00D4FF;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8B949E;
        margin-top: 4px;
    }
    .project-card {
        background: #161B22;
        border: 1px solid #21262D;
        border-left: 3px solid #00D4FF;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
        transition: border-color 0.2s;
    }
    .tag {
        background: #21262D;
        color: #00D4FF;
        border-radius: 4px;
        padding: 2px 10px;
        font-size: 0.75rem;
        margin-right: 6px;
    }
    .section-title {
        color: #00D4FF;
        font-size: 0.75rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────
st.markdown("### 📊 Robinson Matheus")
st.markdown("<p style='color:#8B949E;margin-top:-10px'>Data Analyst · Decision Intelligence</p>", unsafe_allow_html=True)
st.divider()

# ── MÉTRICAS GERAIS ────────────────────────────────────────
st.markdown("<p class='section-title'>Portfolio Overview</p>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("""<div class='metric-card'>
        <div class='metric-value'>4</div>
        <div class='metric-label'>Projetos</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class='metric-card'>
        <div class='metric-value'>94%</div>
        <div class='metric-label'>Melhor Acurácia</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class='metric-card'>
        <div class='metric-value'>15x</div>
        <div class='metric-label'>Ganho de Performance</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown("""<div class='metric-card'>
        <div class='metric-value'>±3%</div>
        <div class='metric-label'>Desvio de Forecast</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── PROJETOS ───────────────────────────────────────────────
st.markdown("<p class='section-title'>Portfolio Cases</p>", unsafe_allow_html=True)

projects = [
    {
        "icon": "🔴",
        "title": "Churn Prediction Model",
        "desc": "Pipeline de ML com 94% de acurácia prevendo churn de clientes, reduzindo attrition em 23%.",
        "tags": ["Python", "Scikit-learn", "Pandas"],
        "kpi": "94% accuracy",
        "page": "pages/01_churn.py"
    },
    {
        "icon": "🟡",
        "title": "Supply Chain Dashboard",
        "desc": "Dashboard em tempo real rastreando logística em 12 armazéns, reduzindo tempo de resposta em 40%.",
        "tags": ["SQL", "Plotly", "DAX"],
        "kpi": "40% faster response",
        "page": "pages/02_supply_chain.py"
    },
    {
        "icon": "🟢",
        "title": "SQL Performance Optimization",
        "desc": "Refatoração de queries legadas reduzindo tempo de execução de 12s para 0.8s em 200+ procedures.",
        "tags": ["PostgreSQL", "Indexing", "Query Tuning"],
        "kpi": "15x faster queries",
        "page": "pages/03_sql_performance.py"
    },
    {
        "icon": "🔵",
        "title": "Revenue Forecasting Engine",
        "desc": "Modelo time-series com Prophet e ARIMA entregando projeções de 6 meses com ±3% de desvio.",
        "tags": ["Prophet", "ARIMA", "Jupyter"],
        "kpi": "±3% deviation",
        "page": "pages/04_revenue_forecast.py"
    },
]

for p in projects:
    tags_html = "".join([f"<span class='tag'>{t}</span>" for t in p["tags"]])
    st.markdown(f"""
    <div class='project-card'>
        <div style='display:flex;justify-content:space-between;align-items:center'>
            <div>
                <span style='font-size:1.1rem;font-weight:600'>{p['icon']} {p['title']}</span>
                <p style='color:#8B949E;margin:6px 0 10px 0;font-size:0.9rem'>{p['desc']}</p>
                {tags_html}
            </div>
            <div style='text-align:right;min-width:120px'>
                <div style='color:#00D4FF;font-weight:700;font-size:1.1rem'>{p['kpi']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("<p style='color:#8B949E;font-size:0.8rem;text-align:center'>NexaCorp Analytics · Dados sintéticos para fins de demonstração</p>", unsafe_allow_html=True)
