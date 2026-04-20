import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="SQL Performance", page_icon="🟢", layout="wide")

st.markdown("""
<style>
    .kpi-card { background: #161B22; border: 1px solid #21262D; border-radius: 10px; padding: 18px; text-align: center; }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #00D4FF; }
    .kpi-delta { font-size: 0.85rem; color: #3FB950; margin-top: 4px; }
    .kpi-label { font-size: 0.78rem; color: #8B949E; margin-top: 2px; }
    .story-box { background: #161B22; border-left: 3px solid #00D4FF; border-radius: 6px; padding: 16px 20px; margin-bottom: 20px; color: #CDD9E5; font-size: 0.92rem; line-height: 1.7; }
    .section-label { color: #00D4FF; font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; }
    .code-box { background: #161B22; border: 1px solid #21262D; border-radius: 6px; padding: 16px; font-family: monospace; font-size: 0.82rem; color: #CDD9E5; white-space: pre-wrap; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("data/query_logs.csv", parse_dates=["execution_date"])

df = load_data()

st.markdown("## 🟢 SQL Performance Optimization")
st.markdown("<p style='color:#8B949E;margin-top:-10px'>PostgreSQL · Query Tuning · Indexing · 200+ Stored Procedures</p>", unsafe_allow_html=True)
st.divider()

st.markdown("<p class='section-label'>O Problema</p>", unsafe_allow_html=True)
st.markdown("""
<div class='story-box'>
O banco de dados da NexaCorp acumulou anos de queries legadas sem revisão. Stored procedures
críticas levavam até 18 segundos para executar, travando relatórios operacionais e atrasando
pipelines de dados. O desafio foi diagnosticar, priorizar e refatorar as 200+ procedures
mais impactantes sem quebrar nada em produção.
<br><br>
<b style='color:#00D4FF'>Resultado:</b> Redução média de 12s para 0.8s de execução — ganho de 15x de performance
com zero incidentes em produção.
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Filtros")
    st.markdown("---")
    min_gain = st.slider("Ganho mínimo (x)", 1.0, 30.0, 5.0, step=0.5)
    only_indexed = st.toggle("Só com índice adicionado", value=False)
    st.markdown("---")
    show_before_after = st.toggle("Comparativo Antes/Depois", value=True)
    show_scatter = st.toggle("Distribuição de Ganhos", value=True)
    show_code = st.toggle("Exemplos de Otimização", value=True)

df["gain"] = df["before_optimization_s"] / df["after_optimization_s"]
df_filtered = df[df["gain"] >= min_gain]
if only_indexed:
    df_filtered = df_filtered[df_filtered["index_added"] == True]

avg_before = df["before_optimization_s"].mean()
avg_after = df["after_optimization_s"].mean()
avg_gain = df["gain"].mean()
pct_indexed = df["index_added"].mean() * 100

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{avg_before:.1f}s</div>
        <div class='kpi-delta' style='color:#F85149'>Tempo médio anterior</div>
        <div class='kpi-label'>Antes da Otimização</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{avg_after:.2f}s</div>
        <div class='kpi-delta'>Tempo médio atual</div>
        <div class='kpi-label'>Depois da Otimização</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{avg_gain:.1f}x</div>
        <div class='kpi-delta'>Ganho médio</div>
        <div class='kpi-label'>Fator de Melhoria</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{pct_indexed:.0f}%</div>
        <div class='kpi-delta'>Das procedures</div>
        <div class='kpi-label'>Receberam Índice</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if show_before_after:
    st.markdown("<p class='section-label'>Comparativo Antes vs Depois — Top 20 Procedures</p>", unsafe_allow_html=True)
    top20 = df.nlargest(20, "gain").sort_values("gain")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top20["procedure_name"], x=top20["before_optimization_s"],
        name="Antes", orientation="h", marker_color="#F85149",
        hovertemplate="<b>%{y}</b><br>Antes: %{x:.2f}s<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        y=top20["procedure_name"], x=top20["after_optimization_s"],
        name="Depois", orientation="h", marker_color="#3FB950",
        hovertemplate="<b>%{y}</b><br>Depois: %{x:.2f}s<extra></extra>"
    ))
    fig.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
                      font=dict(color="#CDD9E5"), height=520, barmode="overlay",
                      margin=dict(l=0, r=0, t=10, b=0),
                      xaxis=dict(gridcolor="#21262D", ticksuffix="s"),
                      yaxis=dict(gridcolor="#21262D", tickfont=dict(size=10)),
                      legend=dict(bgcolor="#161B22"))
    st.plotly_chart(fig, use_container_width=True)

if show_scatter:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Distribuição do Ganho de Performance</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig2 = go.Figure(go.Histogram(
            x=df["gain"], nbinsx=30,
            marker_color="#00D4FF", opacity=0.8,
            hovertemplate="Ganho: %{x:.1f}x<br>Procedures: %{y}<extra></extra>"
        ))
        fig2.add_vline(x=df["gain"].mean(), line_dash="dash", line_color="#F0883E",
                       annotation_text=f"Média {df['gain'].mean():.1f}x",
                       annotation_font_color="#F0883E")
        fig2.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
                           font=dict(color="#CDD9E5"), height=300,
                           margin=dict(l=0, r=0, t=10, b=0),
                           xaxis=dict(gridcolor="#21262D", ticksuffix="x", title="Fator de Ganho"),
                           yaxis=dict(gridcolor="#21262D", title="Nº de Procedures"),
                           showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        scan_before = df["table_scans_before"].mean()
        scan_after = df["table_scans_after"].mean()
        fig3 = go.Figure(go.Bar(
            x=["Table Scans Antes", "Table Scans Depois"],
            y=[scan_before, scan_after],
            marker_color=["#F85149", "#3FB950"],
            text=[f"{scan_before:.0f}", f"{scan_after:.0f}"],
            textposition="outside",
            hovertemplate="%{x}<br>Média: %{y:.1f}<extra></extra>"
        ))
        fig3.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
                           font=dict(color="#CDD9E5"), height=300,
                           margin=dict(l=0, r=0, t=10, b=0),
                           xaxis=dict(gridcolor="#21262D"),
                           yaxis=dict(gridcolor="#21262D", title="Média de Table Scans"),
                           showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

if show_code:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Exemplos de Otimização Aplicada</p>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔴 Antes — Subquery", "🟢 Depois — JOIN", "📋 Índice Adicionado"])

    with tab1:
        st.markdown("<div class='code-box'>SELECT c.customer_id, c.name,\n       (SELECT COUNT(*) FROM transactions t\n        WHERE t.customer_id = c.customer_id) AS total_orders\nFROM customers c\nWHERE c.region = 'Sudeste';\n\n-- ⚠ Execução: ~12.4s | Table scans: 47</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='code-box'>SELECT c.customer_id, c.name,\n       COUNT(t.transaction_id) AS total_orders\nFROM customers c\nLEFT JOIN transactions t ON t.customer_id = c.customer_id\nWHERE c.region = 'Sudeste'\nGROUP BY c.customer_id, c.name;\n\n-- ✅ Execução: ~0.7s | Table scans: 2 | Ganho: 17x</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='code-box'>-- Índice composto adicionado:\nCREATE INDEX idx_transactions_customer_date\n    ON transactions (customer_id, date DESC);\n\nCREATE INDEX idx_customers_region\n    ON customers (region);\n\n-- Resultado: planner passa a usar Index Scan\n-- em vez de Sequential Scan em ambas as tabelas.</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p class='section-label'>Procedures Filtradas</p>", unsafe_allow_html=True)
st.dataframe(
    df_filtered[["procedure_name", "before_optimization_s", "after_optimization_s", "gain", "index_added", "rows_processed"]]
    .rename(columns={
        "procedure_name": "Procedure",
        "before_optimization_s": "Antes (s)",
        "after_optimization_s": "Depois (s)",
        "gain": "Ganho (x)",
        "index_added": "Índice",
        "rows_processed": "Linhas"
    })
    .sort_values("Ganho (x)", ascending=False)
    .head(50),
    use_container_width=True, hide_index=True
)

st.markdown("<br>")
st.markdown("<p style='color:#8B949E;font-size:0.78rem'>* Dados sintéticos da NexaCorp para fins de demonstração.</p>", unsafe_allow_html=True)
