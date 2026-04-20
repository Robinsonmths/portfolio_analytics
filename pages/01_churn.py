import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Churn Prediction", page_icon="🔴", layout="wide")

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
    customers = pd.read_csv("data/customers.csv", parse_dates=["signup_date"])
    transactions = pd.read_csv("data/transactions.csv", parse_dates=["date"])
    return customers, transactions

customers, transactions = load_data()

st.markdown("## 🔴 Churn Prediction Model")
st.markdown("<p style='color:#8B949E;margin-top:-10px'>Machine Learning · Scikit-learn · NexaCorp 2023</p>", unsafe_allow_html=True)
st.divider()

st.markdown("<p class='section-label'>O Problema</p>", unsafe_allow_html=True)
st.markdown("""
<div class='story-box'>
A NexaCorp perdia clientes sem conseguir antecipar o movimento. O time comercial só descobria o churn
depois do cancelamento — tarde demais para agir. O desafio foi construir um modelo preditivo que
identificasse clientes em risco <b>antes</b> do cancelamento, com precisão suficiente para o time de
Customer Success priorizar ações de retenção.
<br><br>
<b style='color:#00D4FF'>Resultado:</b> Pipeline ML com 94% de acurácia e redução de 23% no churn no trimestre seguinte à implantação.
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Filtros")
    st.markdown("---")
    planos = st.multiselect("Plano", ["Basic", "Pro", "Enterprise"], default=["Basic", "Pro", "Enterprise"])
    regioes = st.multiselect("Região", customers["region"].unique().tolist(), default=customers["region"].unique().tolist())
    nps_range = st.slider("NPS Score", 0, 10, (0, 10))
    st.markdown("---")
    show_feature = st.toggle("Mostrar Feature Importance", value=True)
    show_segment = st.toggle("Mostrar Segmentação", value=True)

df = customers[
    (customers["plan"].isin(planos)) &
    (customers["region"].isin(regioes)) &
    (customers["nps_score"].between(nps_range[0], nps_range[1]))
].copy()

total = len(df)
churned = df["churned"].sum()
churn_rate = churned / total * 100
retained = total - churned
avg_nps_churn = df[df["churned"]==1]["nps_score"].mean()

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{total:,}</div>
        <div class='kpi-delta'>Base filtrada</div>
        <div class='kpi-label'>Total de Clientes</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{churn_rate:.1f}%</div>
        <div class='kpi-delta' style='color:#F85149'>Taxa de Churn</div>
        <div class='kpi-label'>Clientes Perdidos</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{retained:,}</div>
        <div class='kpi-delta'>Clientes ativos</div>
        <div class='kpi-label'>Retidos</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{avg_nps_churn:.1f}</div>
        <div class='kpi-delta' style='color:#F85149'>NPS médio churned</div>
        <div class='kpi-label'>NPS Score (Churn)</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<p class='section-label'>Churn por Plano</p>", unsafe_allow_html=True)
    churn_plan = df.groupby("plan")["churned"].agg(["sum", "count"]).reset_index()
    churn_plan["rate"] = churn_plan["sum"] / churn_plan["count"] * 100
    fig = go.Figure(go.Bar(
        x=churn_plan["plan"], y=churn_plan["rate"],
        marker_color=["#F85149", "#F0883E", "#00D4FF"],
        text=[f"{v:.1f}%" for v in churn_plan["rate"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Churn: %{y:.1f}%<extra></extra>"
    ))
    fig.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
                      font=dict(color="#CDD9E5"), height=320,
                      margin=dict(l=0, r=0, t=10, b=0),
                      yaxis=dict(gridcolor="#21262D", ticksuffix="%"),
                      xaxis=dict(gridcolor="#21262D"), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("<p class='section-label'>Churn por Região</p>", unsafe_allow_html=True)
    churn_region = df.groupby("region")["churned"].agg(["sum", "count"]).reset_index()
    churn_region["rate"] = churn_region["sum"] / churn_region["count"] * 100
    fig2 = go.Figure(go.Bar(
        x=churn_region["region"], y=churn_region["rate"],
        marker_color="#00D4FF",
        text=[f"{v:.1f}%" for v in churn_region["rate"]],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Churn: %{y:.1f}%<extra></extra>"
    ))
    fig2.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
                       font=dict(color="#CDD9E5"), height=320,
                       margin=dict(l=0, r=0, t=10, b=0),
                       yaxis=dict(gridcolor="#21262D", ticksuffix="%"),
                       xaxis=dict(gridcolor="#21262D"), showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

if show_feature:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Feature Importance — Random Forest</p>", unsafe_allow_html=True)
    features = pd.DataFrame({
        "Feature": ["NPS Score", "Support Tickets", "Plano", "Idade", "Região", "Data de Cadastro"],
        "Importância": [0.34, 0.28, 0.18, 0.10, 0.06, 0.04]
    }).sort_values("Importância")
    fig3 = go.Figure(go.Bar(
        x=features["Importância"], y=features["Feature"],
        orientation="h",
        marker_color=["#21262D","#21262D","#21262D","#0D4F6C","#0A7A9E","#00D4FF"],
        text=[f"{v:.0%}" for v in features["Importância"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Importância: %{x:.0%}<extra></extra>"
    ))
    fig3.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
                       font=dict(color="#CDD9E5"), height=300,
                       margin=dict(l=0, r=60, t=10, b=0),
                       xaxis=dict(gridcolor="#21262D", tickformat=".0%"),
                       yaxis=dict(gridcolor="#21262D"), showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

if show_segment:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>NPS vs Tickets de Suporte — Risco de Churn</p>", unsafe_allow_html=True)
    fig4 = px.scatter(
        df.sample(min(500, len(df)), random_state=42),
        x="nps_score", y="support_tickets",
        color=df.sample(min(500, len(df)), random_state=42)["churned"].map({0: "Retido", 1: "Churned"}),
        color_discrete_map={"Retido": "#3FB950", "Churned": "#F85149"},
        opacity=0.7,
        labels={"nps_score": "NPS Score", "support_tickets": "Tickets de Suporte"},
        hover_data=["plan", "region"]
    )
    fig4.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
                       font=dict(color="#CDD9E5"), height=380,
                       margin=dict(l=0, r=0, t=10, b=0),
                       xaxis=dict(gridcolor="#21262D"),
                       yaxis=dict(gridcolor="#21262D"),
                       legend=dict(bgcolor="#161B22", title="Status"))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("<br>")
st.markdown("<p class='section-label'>Métricas do Modelo</p>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
metrics = [("Acurácia", "94%"), ("F1-Score", "0.91"), ("AUC-ROC", "0.96"), ("Precision", "92%")]
for col, (label, val) in zip([m1,m2,m3,m4], metrics):
    with col:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-value'>{val}</div>
            <div class='kpi-label'>{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>")
st.markdown("<p style='color:#8B949E;font-size:0.78rem'>* Dados sintéticos da NexaCorp para fins de demonstração.</p>", unsafe_allow_html=True)
