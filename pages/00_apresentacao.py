import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="NexaCorp | Apresentação", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .chapter-header {
        background: linear-gradient(135deg, #161B22 0%, #0E1117 100%);
        border: 1px solid #21262D;
        border-left: 4px solid #00D4FF;
        border-radius: 10px;
        padding: 28px 32px;
        margin-bottom: 24px;
    }
    .chapter-number {
        color: #00D4FF;
        font-size: 0.75rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .chapter-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #FAFAFA;
        margin-bottom: 10px;
    }
    .chapter-subtitle {
        color: #8B949E;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .problem-box {
        background: #1A0A0A;
        border: 1px solid #3D1A1A;
        border-left: 4px solid #F85149;
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 16px;
        color: #CDD9E5;
        font-size: 0.92rem;
        line-height: 1.7;
    }
    .solution-box {
        background: #0A1A0E;
        border: 1px solid #1A3D22;
        border-left: 4px solid #3FB950;
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 16px;
        color: #CDD9E5;
        font-size: 0.92rem;
        line-height: 1.7;
    }
    .insight-box {
        background: #161B22;
        border: 1px solid #21262D;
        border-left: 4px solid #00D4FF;
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 16px;
        color: #CDD9E5;
        font-size: 0.92rem;
        line-height: 1.7;
    }
    .kpi-card {
        background: #161B22;
        border: 1px solid #21262D;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .kpi-value { font-size: 2.2rem; font-weight: 700; color: #00D4FF; }
    .kpi-label { font-size: 0.78rem; color: #8B949E; margin-top: 4px; }
    .kpi-delta { font-size: 0.82rem; color: #3FB950; margin-top: 4px; }
    .divider-chapter {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #00D4FF, transparent);
        margin: 48px 0;
    }
    .section-label {
        color: #00D4FF;
        font-size: 0.72rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .closing-card {
        background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
        border: 1px solid #00D4FF;
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        margin-top: 32px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_all():
    customers = pd.read_csv("data/customers.csv")
    logistics = pd.read_csv("data/logistics.csv", parse_dates=["date"])
    query_logs = pd.read_csv("data/query_logs.csv")
    revenue = pd.read_csv("data/revenue_monthly.csv", parse_dates=["month"])
    warehouses = pd.read_csv("data/warehouses.csv")
    return customers, logistics, query_logs, revenue, warehouses

customers, logistics, query_logs, revenue, warehouses = load_all()

# ── ABERTURA ───────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 48px 0 32px 0;'>
    <p style='color:#00D4FF;font-size:0.78rem;letter-spacing:3px;text-transform:uppercase;margin-bottom:12px'>Estudo de Caso</p>
    <h1 style='font-size:3rem;font-weight:800;color:#FAFAFA;margin-bottom:16px'>NexaCorp Analytics</h1>
    <p style='color:#8B949E;font-size:1.1rem;max-width:600px;margin:0 auto;line-height:1.7'>
        Em 2023, a NexaCorp enfrentava quatro problemas críticos que ameaçavam
        sua operação e crescimento. Esta é a história de como os dados
        transformaram cada um deles em vantagem competitiva.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""<div class='kpi-card'>
        <div class='kpi-value'>23%</div>
        <div class='kpi-delta'>↓ Churn reduzido</div>
        <div class='kpi-label'>Retenção de Clientes</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class='kpi-card'>
        <div class='kpi-value'>40%</div>
        <div class='kpi-delta'>↓ Tempo de resposta</div>
        <div class='kpi-label'>Operação Logística</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class='kpi-card'>
        <div class='kpi-value'>15x</div>
        <div class='kpi-delta'>↑ Performance</div>
        <div class='kpi-label'>Banco de Dados</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown("""<div class='kpi-card'>
        <div class='kpi-value'>±3%</div>
        <div class='kpi-delta'>Desvio de forecast</div>
        <div class='kpi-label'>Previsão de Receita</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<hr class='divider-chapter'>", unsafe_allow_html=True)

# ── CAPÍTULO 1 — CHURN ─────────────────────────────────────
st.markdown("""
<div class='chapter-header'>
    <div class='chapter-number'>Capítulo 01</div>
    <div class='chapter-title'>O Cliente Estava Indo Embora</div>
    <div class='chapter-subtitle'>A NexaCorp perdia clientes silenciosamente. Sem alertas, sem antecipação — só descobria o cancelamento depois que já era tarde demais para agir.</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("""
    <div class='problem-box'>
    <b style='color:#F85149'>⚠ O Problema</b><br><br>
    A taxa de churn chegou a <b>23%</b> no trimestre — quase 1 em cada 4 clientes cancelando.
    O time comercial só descobria o movimento após o cancelamento, sem tempo de reação.
    Não havia modelo preditivo, não havia segmentação de risco, não havia processo de retenção estruturado.
    </div>
    <div class='solution-box'>
    <b style='color:#3FB950'>✓ A Solução</b><br><br>
    Pipeline de Machine Learning com <b>Random Forest</b> treinado sobre histórico de comportamento —
    NPS Score, tickets de suporte e frequência de uso. O modelo passou a gerar um score de risco
    semanal para cada cliente, permitindo ação proativa do time de Customer Success.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<p class='section-label'>Churn por Plano</p>", unsafe_allow_html=True)
    churn_plan = customers.groupby("plan")["churned"].agg(["sum","count"]).reset_index()
    churn_plan["rate"] = churn_plan["sum"] / churn_plan["count"] * 100
    fig = go.Figure(go.Bar(
        x=churn_plan["plan"], y=churn_plan["rate"],
        marker_color=["#F85149","#F0883E","#00D4FF"],
        text=[f"{v:.1f}%" for v in churn_plan["rate"]],
        textposition="outside",
    ))
    fig.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
                      font=dict(color="#CDD9E5"), height=280,
                      margin=dict(l=0,r=0,t=10,b=0),
                      yaxis=dict(gridcolor="#21262D", ticksuffix="%"),
                      xaxis=dict(gridcolor="#21262D"), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class='insight-box'>
<b style='color:#00D4FF'>📌 Conclusão do Capítulo</b><br><br>
Com o modelo em produção, o time de CS passou a priorizar os <b>top 200 clientes em risco</b> semanalmente.
No trimestre seguinte, a taxa de churn caiu <b>23%</b> — resultado direto de ações de retenção
guiadas pelo score preditivo. Acurácia do modelo: <b>94%</b> · AUC-ROC: <b>0.96</b>.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider-chapter'>", unsafe_allow_html=True)

# ── CAPÍTULO 2 — SUPPLY CHAIN ──────────────────────────────
st.markdown("""
<div class='chapter-header'>
    <div class='chapter-number'>Capítulo 02</div>
    <div class='chapter-title'>A Operação Estava Cega</div>
    <div class='chapter-subtitle'>12 armazéns, milhares de envios por mês — e o time de operações gerenciando tudo por relatórios diários em Excel. Atrasos eram descobertos horas depois do ocorrido.</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("""
    <div class='problem-box'>
    <b style='color:#F85149'>⚠ O Problema</b><br><br>
    O tempo médio de detecção de um atraso crítico era de <b>6 horas</b>.
    Sem visibilidade em tempo real, decisões de remanejamento de estoque e
    acionamento de transportadoras alternativas chegavam sempre tarde.
    SLA sendo quebrado sistematicamente sem que ninguém percebesse.
    </div>
    <div class='solution-box'>
    <b style='color:#3FB950'>✓ A Solução</b><br><br>
    Dashboard em tempo real conectado via <b>DirectQuery</b> ao banco de dados operacional,
    atualizando a cada 15 minutos. KPIs de SLA, status por armazém e performance por
    transportadora disponíveis em uma única tela. Alertas automáticos para desvios críticos.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<p class='section-label'>Status dos Envios</p>", unsafe_allow_html=True)
    status_counts = logistics["status"].value_counts().reset_index()
    status_counts.columns = ["status","count"]
    color_map = {"Entregue":"#3FB950","Em trânsito":"#00D4FF","Atrasado":"#F0883E","Extraviado":"#F85149"}
    colors = [color_map.get(s,"#8B949E") for s in status_counts["status"]]
    fig2 = go.Figure(go.Pie(
        labels=status_counts["status"], values=status_counts["count"],
        marker_colors=colors, hole=0.5,
    ))
    fig2.update_layout(paper_bgcolor="#0E1117", font=dict(color="#CDD9E5"),
                       height=280, margin=dict(l=0,r=0,t=10,b=0),
                       legend=dict(bgcolor="#161B22"))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
<div class='insight-box'>
<b style='color:#00D4FF'>📌 Conclusão do Capítulo</b><br><br>
O tempo de detecção de incidentes caiu de <b>6 horas para menos de 1 hora</b> — redução de <b>40%</b>
no tempo médio de resposta operacional. Armazéns com utilização acima de 90% passaram a
receber alertas automáticos, evitando gargalos antes que afetassem entregas.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider-chapter'>", unsafe_allow_html=True)

# ── CAPÍTULO 3 — SQL ───────────────────────────────────────
st.markdown("""
<div class='chapter-header'>
    <div class='chapter-number'>Capítulo 03</div>
    <div class='chapter-title'>O Banco de Dados Travou a Empresa</div>
    <div class='chapter-subtitle'>Relatórios que deveriam sair em segundos levavam minutos. Pipelines de dados atrasando decisões. O problema estava nas queries — e ninguém tinha parado para olhar.</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("""
    <div class='problem-box'>
    <b style='color:#F85149'>⚠ O Problema</b><br><br>
    Stored procedures críticas com tempo médio de <b>12 segundos</b> de execução.
    Queries legadas com subqueries correlacionadas, table scans desnecessários e
    ausência de índices nas colunas mais filtradas. O banco cresceu sem revisão
    técnica por anos — e a dívida técnica cobrou o preço.
    </div>
    <div class='solution-box'>
    <b style='color:#3FB950'>✓ A Solução</b><br><br>
    Diagnóstico via <b>pg_stat_statements</b> para identificar as queries de maior impacto acumulado.
    Refatoração de subqueries para JOINs, criação de índices compostos nas colunas críticas
    e reescrita de cursores para operações set-based. Zero incidentes em produção graças
    ao script de validação de equivalência de resultados.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<p class='section-label'>Tempo de Execução — Antes vs Depois</p>", unsafe_allow_html=True)
    query_logs["gain"] = query_logs["before_optimization_s"] / query_logs["after_optimization_s"]
    top10 = query_logs.nlargest(10, "gain").sort_values("gain")
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(y=top10["procedure_name"], x=top10["before_optimization_s"],
                          name="Antes", orientation="h", marker_color="#F85149"))
    fig3.add_trace(go.Bar(y=top10["procedure_name"], x=top10["after_optimization_s"],
                          name="Depois", orientation="h", marker_color="#3FB950"))
    fig3.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
                       font=dict(color="#CDD9E5"), height=320, barmode="overlay",
                       margin=dict(l=0,r=0,t=10,b=0),
                       xaxis=dict(gridcolor="#21262D", ticksuffix="s"),
                       yaxis=dict(gridcolor="#21262D", tickfont=dict(size=9)),
                       legend=dict(bgcolor="#161B22"))
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("""
<div class='insight-box'>
<b style='color:#00D4FF'>📌 Conclusão do Capítulo</b><br><br>
Tempo médio de execução reduzido de <b>12s para 0.8s</b> — ganho de <b>15x</b> de performance.
200+ stored procedures refatoradas com script de validação garantindo equivalência total dos resultados.
Os pipelines de dados voltaram a rodar dentro das janelas operacionais.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider-chapter'>", unsafe_allow_html=True)

# ── CAPÍTULO 4 — FORECAST ──────────────────────────────────
st.markdown("""
<div class='chapter-header'>
    <div class='chapter-number'>Capítulo 04</div>
    <div class='chapter-title'>Ninguém Sabia o Futuro da Receita</div>
    <div class='chapter-subtitle'>Budget aprovado com base em feeling. Contratações sem previsão de caixa. Estoque dimensionado no chute. A NexaCorp crescia — mas às cegas.</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("""
    <div class='problem-box'>
    <b style='color:#F85149'>⚠ O Problema</b><br><br>
    Sem modelo de forecasting, o planejamento financeiro era reativo.
    Decisões de budget para o trimestre seguinte eram tomadas com base
    na intuição dos gestores — sem base estatística, sem intervalo de
    confiança, sem cenários alternativos.
    </div>
    <div class='solution-box'>
    <b style='color:#3FB950'>✓ A Solução</b><br><br>
    Engine de forecasting com <b>Prophet + ARIMA</b> entregando projeções de 6 meses
    com intervalo de confiança configurável. Simulador de cenários pessimista,
    neutro e otimista integrado ao dashboard financeiro. Retraining automático
    mensal para manter o modelo calibrado.
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<p class='section-label'>Histórico de Receita e Tendência</p>", unsafe_allow_html=True)
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=revenue["month"], y=revenue["revenue"],
                              name="Receita Real", mode="lines",
                              line=dict(color="#00D4FF", width=2.5),
                              fill="tozeroy", fillcolor="rgba(0,212,255,0.07)"))
    fig4.add_trace(go.Scatter(x=revenue["month"], y=revenue["profit"],
                              name="Lucro", mode="lines",
                              line=dict(color="#3FB950", width=2)))
    fig4.update_layout(paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
                       font=dict(color="#CDD9E5"), height=280,
                       margin=dict(l=0,r=0,t=10,b=0),
                       xaxis=dict(gridcolor="#21262D"),
                       yaxis=dict(gridcolor="#21262D", tickprefix="R$ ", tickformat=",.0f"),
                       legend=dict(bgcolor="#161B22"))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
<div class='insight-box'>
<b style='color:#00D4FF'>📌 Conclusão do Capítulo</b><br><br>
Modelo adotado pelo time financeiro como <b>referência oficial de planejamento trimestral</b>.
Desvio médio de <b>±3%</b> em projeções de 6 meses — dentro do threshold de 5% exigido pelo CFO.
Pela primeira vez, o budget foi aprovado com base estatística e cenários documentados.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider-chapter'>", unsafe_allow_html=True)

# ── ENCERRAMENTO ───────────────────────────────────────────
st.markdown("""
<div class='closing-card'>
    <p style='color:#00D4FF;font-size:0.75rem;letter-spacing:3px;text-transform:uppercase;margin-bottom:16px'>Impacto Consolidado</p>
    <h2 style='font-size:2rem;font-weight:800;color:#FAFAFA;margin-bottom:8px'>Quatro Problemas. Quatro Soluções.</h2>
    <p style='color:#8B949E;font-size:0.95rem;max-width:560px;margin:0 auto 32px auto;line-height:1.7'>
        Em menos de um ano, dados estruturados transformaram decisões reativas
        em vantagem competitiva real para a NexaCorp.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
impactos = [
    ("🔴", "Churn", "−23%", "Redução de cancelamentos"),
    ("🟡", "Supply Chain", "−40%", "Tempo de resposta operacional"),
    ("🟢", "SQL", "15x", "Ganho de performance"),
    ("🔵", "Forecast", "±3%", "Desvio de projeção"),
]
for col, (icon, title, value, label) in zip([c1,c2,c3,c4], impactos):
    with col:
        st.markdown(f"""<div class='kpi-card'>
            <div style='font-size:1.5rem'>{icon}</div>
            <div style='color:#8B949E;font-size:0.75rem;margin:4px 0'>{title}</div>
            <div class='kpi-value'>{value}</div>
            <div class='kpi-label'>{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br><br>")
st.markdown("<p style='color:#8B949E;font-size:0.78rem;text-align:center'>NexaCorp Analytics · Dados sintéticos para fins de demonstração · Robinson Matheus</p>", unsafe_allow_html=True)
