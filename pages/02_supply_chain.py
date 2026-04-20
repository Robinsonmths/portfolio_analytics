import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Supply Chain", page_icon="🟡", layout="wide")

st.markdown("""
<style>
    .kpi-card { background: #161B22; border: 1px solid #21262D; border-radius: 10px; padding: 18px; text-align: center; }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #00D4FF; }
    .kpi-delta { font-size: 0.85rem; color: #3FB950; margin-top: 4px; }
    .kpi-label { font-size: 0.78rem; color: #8B949E; margin-top: 2px; }
    .story-box { background: #161B22; border-left: 3px solid #00D4FF; border-radius: 6px; padding: 16px 20px; margin-bottom: 20px; color: #CDD9E5; font-size: 0.92rem; line-height: 1.7; }
    .section-label { color: #00D4FF; font-size: 0.72rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    warehouses = pd.read_csv("data/warehouses.csv")
    logistics = pd.read_csv("data/logistics.csv", parse_dates=["date"])
    return warehouses, logistics

warehouses, logistics = load_data()

st.markdown("## 🟡 Supply Chain Dashboard")
st.markdown("<p style='color:#8B949E;margin-top:-10px'>Real-time Analytics · SQL + Plotly · 12 Armazéns · NexaCorp 2023</p>", unsafe_allow_html=True)
st.divider()

st.markdown("<p class='section-label'>O Problema</p>", unsafe_allow_html=True)
st.markdown("""
<div class='story-box'>
O time de operações da NexaCorp gerenciava 12 armazéns via relatórios diários em Excel —
atrasos e extraviados eram detectados horas depois do ocorrido. O desafio foi construir
um dashboard em tempo real que centralizasse todos os indicadores logísticos e permitisse
resposta imediata a desvios operacionais.
<br><br>
<b style='color:#00D4FF'>Resultado:</b> Redução de 40% no tempo médio de resposta a incidentes logísticos,
com alertas automáticos para SLA em risco.
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Filtros")
    st.markdown("---")
    regioes = st.multiselect("Região", logistics["destination_region"].unique().tolist(),
                              default=logistics["destination_region"].unique().tolist())
    carriers = st.multiselect("Transportadora", logistics["carrier"].unique().tolist(),
                               default=logistics["carrier"].unique().tolist())
    status_list = st.multiselect("Status", logistics["status"].unique().tolist(),
                                  default=logistics["status"].unique().tolist())
    date_range = st.date_input("Período", [logistics["date"].min(), logistics["date"].max()])
    st.markdown("---")
    show_map = st.toggle("Mostrar Utilização dos Armazéns", value=True)
    show_sla = st.toggle("Mostrar Análise de SLA", value=True)

df = logistics[
    (logistics["destination_region"].isin(regioes)) &
    (logistics["carrier"].isin(carriers)) &
    (logistics["status"].isin(status_list))
].copy()

if len(date_range) == 2:
    df = df[(df["date"] >= pd.Timestamp(date_range[0])) & (df["date"] <= pd.Timestamp(date_range[1]))]

total_envios = len(df)
on_time_rate = df["on_time"].mean() * 100
atrasados = (df["status"] == "Atrasado").sum()
extraviados = (df["status"] == "Extraviado").sum()

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{total_envios:,}</div>
        <div class='kpi-delta'>No período</div>
        <div class='kpi-label'>Total de Envios</div>
    </div>""", unsafe_allow_html=True)
with k2:
    color = "3FB950" if on_time_rate >= 80 else "F85149"
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{on_time_rate:.1f}%</div>
        <div class='kpi-delta' style='color:#{color}'>On-Time Delivery</div>
        <div class='kpi-label'>Taxa de Pontualidade</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{atrasados:,}</div>
        <div class='kpi-delta' style='color:#F85149'>Requer atenção</div>
        <div class='kpi-label'>Envios Atrasados</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{extraviados:,}</div>
        <div class='kpi-delta' style='color:#F85149'>Crítico</div>
        <div class='kpi-label'>Extraviados</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<p class='section-label'>Status dos Envios</p>", unsafe_allow_html=True)
    status_counts = df["status"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]
    color_map = {"Entregue": "#3FB950", "Em trânsito": "#00D4FF", "Atrasado": "#F0883E", "Extraviado": "#F85149"}
    colors = [color_map.get(s, "#8B949E") for s in status_counts["status"]]
    fig = go.Figure(go.Pie(
        labels=status_counts["status"], values=status_counts["count"],
        marker_colors=colors, hole=0.5,
        hovertemplate="<b>%{label}</b><br>%{value:,} envios<br>%{percent}<extra></extra>"
    ))
    fig.update_layout(paper_bgcolor="#0E1117", font=dict(color="#CDD9E5"),
                      height=320, margin=dict(l=0, r=0, t=10, b=0),
                      legend=dict(bgcolor="#161B22"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("<p class='section-label'>Performance por Transportadora</p>", unsafe_allow_html=True)
    carrier_perf = df.groupby("carrier")["on_time"].mean().reset_index()
    carrier_perf["on_time"] = carrier_perf["on_time"] * 100
    carrier_perf = carrier_perf.sort_values("on_time")
    colors2 = ["#F85149" if v < 75 else "#F0883E" if v < 85 else "#3FB950" for v in carrier_perf["on_time"]]
    fig2 = go.Figure(go.Bar(
        x=carrier_perf["on_time"], y=carrier_perf["carrier"],
        orientation="h", marker_color=colors2,
        text=[f"{v:.1f}%" for v in carrier_perf["on_time"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>On-time: %{x:.1f}%<extra></extra>"
    ))
    fig2.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
                       font=dict(color="#CDD9E5"), height=320,
                       margin=dict(l=0, r=60, t=10, b=0),
                       xaxis=dict(gridcolor="#21262D", ticksuffix="%", range=[0, 115]),
                       yaxis=dict(gridcolor="#21262D"), showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

if show_map:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Utilização dos Armazéns</p>", unsafe_allow_html=True)
    wh = warehouses.copy()
    wh["utilization_pct_display"] = wh["utilization_pct"] * 100
    fig3 = go.Figure(go.Bar(
        x=wh["city"], y=wh["utilization_pct_display"],
        marker_color=["#F85149" if v > 90 else "#F0883E" if v > 80 else "#3FB950" for v in wh["utilization_pct_display"]],
        text=[f"{v:.0f}%" for v in wh["utilization_pct_display"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Utilização: %{y:.1f}%<extra></extra>"
    ))
    fig3.add_hline(y=90, line_dash="dash", line_color="#F85149", annotation_text="Limite crítico 90%", annotation_font_color="#F85149")
    fig3.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
                       font=dict(color="#CDD9E5"), height=340,
                       margin=dict(l=0, r=0, t=10, b=0),
                       xaxis=dict(gridcolor="#21262D"),
                       yaxis=dict(gridcolor="#21262D", ticksuffix="%", range=[0, 115]),
                       showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

if show_sla:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Dias de Entrega vs SLA por Região</p>", unsafe_allow_html=True)
    sla_region = df.groupby("destination_region").agg(
        avg_delivery=("delivery_days", "mean"),
        avg_sla=("sla_days", "mean")
    ).reset_index()
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(name="Dias Reais", x=sla_region["destination_region"],
                          y=sla_region["avg_delivery"], marker_color="#F0883E"))
    fig4.add_trace(go.Bar(name="SLA Contratado", x=sla_region["destination_region"],
                          y=sla_region["avg_sla"], marker_color="#00D4FF"))
    fig4.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
                       font=dict(color="#CDD9E5"), height=340, barmode="group",
                       margin=dict(l=0, r=0, t=10, b=0),
                       xaxis=dict(gridcolor="#21262D"),
                       yaxis=dict(gridcolor="#21262D", ticksuffix=" dias"),
                       legend=dict(bgcolor="#161B22"))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("<br>")
st.markdown("<p style='color:#8B949E;font-size:0.78rem'>* Dados sintéticos da NexaCorp para fins de demonstração.</p>", unsafe_allow_html=True)
