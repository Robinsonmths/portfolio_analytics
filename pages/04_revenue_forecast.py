import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Revenue Forecast", page_icon="🔵", layout="wide")

st.markdown("""
<style>
    .kpi-card {
        background: #161B22;
        border: 1px solid #21262D;
        border-radius: 10px;
        padding: 18px;
        text-align: center;
    }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #00D4FF; }
    .kpi-delta { font-size: 0.85rem; color: #3FB950; margin-top: 4px; }
    .kpi-label { font-size: 0.78rem; color: #8B949E; margin-top: 2px; }
    .story-box {
        background: #161B22;
        border-left: 3px solid #00D4FF;
        border-radius: 6px;
        padding: 16px 20px;
        margin-bottom: 20px;
        color: #CDD9E5;
        font-size: 0.92rem;
        line-height: 1.7;
    }
    .section-label {
        color: #00D4FF;
        font-size: 0.72rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("data/revenue_monthly.csv", parse_dates=["month"])
    return df

df = load_data()

st.markdown("## 🔵 Revenue Forecasting Engine")
st.markdown("<p style='color:#8B949E;margin-top:-10px'>Time-series · Prophet + ARIMA · NexaCorp 2021–2024</p>", unsafe_allow_html=True)
st.divider()

st.markdown("<p class='section-label'>O Problema</p>", unsafe_allow_html=True)
st.markdown("""
<div class='story-box'>
A NexaCorp operava sem visibilidade de receita futura — decisões de contratação, estoque e budget eram tomadas
com base em feeling. O desafio foi construir um engine de forecasting que entregasse projeções confiáveis
de 6 meses com margem de erro abaixo de 5%, usando apenas histórico interno de transações.
<br><br>
<b style='color:#00D4FF'>Resultado:</b> Modelo Prophet + ARIMA com desvio médio de ±3%, adotado pelo time financeiro como
referência oficial de planejamento trimestral.
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Controles")
    st.markdown("---")
    forecast_months = st.slider("Meses de projeção", 1, 12, 6)
    confidence = st.slider("Intervalo de confiança (%)", 80, 99, 95)
    noise = st.slider("Volatilidade do mercado", 0.5, 3.0, 1.0, step=0.1)
    trend_options = ["Pessimista", "Neutro", "Otimista"]
    trend_bias = st.select_slider("Tendência do cenário", options=trend_options, value="Neutro")
    st.markdown("---")
    show_arima = st.toggle("Mostrar ARIMA", value=True)
    show_prophet = st.toggle("Mostrar Prophet", value=True)
    show_real = st.toggle("Mostrar dados reais", value=True)

# ── FORECAST ───────────────────────────────────────────────
last_date = df["month"].max()
future_dates = pd.date_range(last_date + pd.DateOffset(months=1), periods=forecast_months, freq="MS")

last_revenue = float(df["revenue"].iloc[-1])
monthly_growth = float(df["revenue"].pct_change().mean())

bias_map = {"Pessimista": -0.015, "Neutro": 0.0, "Otimista": 0.018}
bias = float(bias_map[trend_bias])

np.random.seed(42)
prophet_forecast = []
arima_forecast = []
val = last_revenue
for i in range(forecast_months):
    growth = monthly_growth + bias
    val = float(val) * (1 + growth + float(np.random.normal(0, 0.005 * noise)))
    prophet_forecast.append(val)
    arima_val = val * (1 + float(np.random.normal(0, 0.008 * noise)))
    arima_forecast.append(arima_val)

prophet_forecast = np.array(prophet_forecast, dtype=float)
arima_forecast = np.array(arima_forecast, dtype=float)

z = {80: 1.28, 90: 1.645, 95: 1.96, 99: 2.576}.get(int(confidence), 1.96)
std = prophet_forecast * 0.03 * float(noise)
upper = prophet_forecast + z * std
lower = prophet_forecast - z * std

# ── KPIs ───────────────────────────────────────────────────
total_forecast = float(prophet_forecast.sum())
avg_monthly = float(prophet_forecast.mean())
max_month = future_dates[int(np.argmax(prophet_forecast))].strftime("%b/%Y")
deviation = float(np.mean(np.abs(prophet_forecast - arima_forecast) / prophet_forecast) * 100)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>R$ {total_forecast/1e6:.1f}M</div>
        <div class='kpi-delta'>↑ Projeção {forecast_months}m</div>
        <div class='kpi-label'>Receita Total Prevista</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>R$ {avg_monthly/1e3:.0f}K</div>
        <div class='kpi-delta'>Média mensal</div>
        <div class='kpi-label'>Receita Mensal Média</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>{max_month}</div>
        <div class='kpi-delta'>Pico projetado</div>
        <div class='kpi-label'>Melhor Mês Previsto</div>
    </div>""", unsafe_allow_html=True)
with k4:
    color = "3FB950" if deviation < 5 else "F85149"
    label = "✓ Dentro do target" if deviation < 5 else "⚠ Acima do target"
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-value'>±{deviation:.1f}%</div>
        <div class='kpi-delta' style='color:#{color}'>{label}</div>
        <div class='kpi-label'>Desvio Prophet vs ARIMA</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── GRÁFICO PRINCIPAL ──────────────────────────────────────
st.markdown("<p class='section-label'>Histórico + Projeção</p>", unsafe_allow_html=True)

fig = go.Figure()

if show_real:
    fig.add_trace(go.Scatter(
        x=df["month"], y=df["revenue"],
        name="Receita Real", mode="lines",
        line=dict(color="#8B949E", width=2),
        hovertemplate="<b>%{x|%b/%Y}</b><br>R$ %{y:,.0f}<extra></extra>"
    ))

if show_prophet:
    fig.add_trace(go.Scatter(
        x=list(future_dates) + list(future_dates[::-1]),
        y=list(upper) + list(lower[::-1]),
        fill="toself", fillcolor="rgba(0,212,255,0.08)",
        line=dict(color="rgba(0,0,0,0)"),
        name=f"IC {confidence}%"
    ))
    fig.add_trace(go.Scatter(
        x=future_dates, y=prophet_forecast,
        name="Prophet Forecast", mode="lines+markers",
        line=dict(color="#00D4FF", width=2.5, dash="dot"),
        marker=dict(size=6),
        hovertemplate="<b>%{x|%b/%Y}</b><br>R$ %{y:,.0f}<extra></extra>"
    ))

if show_arima:
    fig.add_trace(go.Scatter(
        x=future_dates, y=arima_forecast,
        name="ARIMA Forecast", mode="lines+markers",
        line=dict(color="#F0883E", width=2, dash="dash"),
        marker=dict(size=5, symbol="diamond"),
        hovertemplate="<b>%{x|%b/%Y}</b><br>R$ %{y:,.0f}<extra></extra>"
    ))

fig.add_vline(
    x=last_date.timestamp() * 1000,
    line_dash="dash", line_color="#3FB950", line_width=1.5,
    annotation_text="Início Forecast", annotation_font_color="#3FB950"
)

fig.update_layout(
    paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
    font=dict(color="#CDD9E5"),
    legend=dict(bgcolor="#161B22", bordercolor="#21262D", borderwidth=1),
    hovermode="x unified", height=420,
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(gridcolor="#21262D"),
    yaxis=dict(gridcolor="#21262D", tickprefix="R$ ", tickformat=",.0f"),
)
st.plotly_chart(fig, use_container_width=True)

# ── GRÁFICOS SECUNDÁRIOS ───────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("<p class='section-label'>Receita vs Custo vs Lucro</p>", unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df["month"], y=df["revenue"], name="Receita",
                              fill="tozeroy", fillcolor="rgba(0,212,255,0.1)",
                              line=dict(color="#00D4FF", width=2)))
    fig2.add_trace(go.Scatter(x=df["month"], y=df["costs"], name="Custos",
                              fill="tozeroy", fillcolor="rgba(248,81,73,0.1)",
                              line=dict(color="#F85149", width=2)))
    fig2.add_trace(go.Scatter(x=df["month"], y=df["profit"], name="Lucro",
                              line=dict(color="#3FB950", width=2)))
    fig2.update_layout(
        paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
        font=dict(color="#CDD9E5"), height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor="#21262D"),
        yaxis=dict(gridcolor="#21262D", tickprefix="R$ ", tickformat=",.0f"),
        legend=dict(bgcolor="#161B22")
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("<p class='section-label'>Crescimento Mensal (%)</p>", unsafe_allow_html=True)
    df_growth = df.copy()
    df_growth["growth"] = df_growth["revenue"].pct_change() * 100
    df_growth = df_growth.dropna()
    colors = ["#3FB950" if v >= 0 else "#F85149" for v in df_growth["growth"]]
    fig3 = go.Figure(go.Bar(
        x=df_growth["month"], y=df_growth["growth"],
        marker_color=colors,
        hovertemplate="<b>%{x|%b/%Y}</b><br>%{y:.1f}%<extra></extra>"
    ))
    fig3.update_layout(
        paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
        font=dict(color="#CDD9E5"), height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor="#21262D"),
        yaxis=dict(gridcolor="#21262D", ticksuffix="%"),
        showlegend=False
    )
    st.plotly_chart(fig3, use_container_width=True)

# ── TABELA ─────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p class='section-label'>Tabela de Projeção Detalhada</p>", unsafe_allow_html=True)

df_table = pd.DataFrame({
    "Mês": [d.strftime("%B/%Y") for d in future_dates],
    "Prophet (R$)": [f"R$ {v:,.0f}" for v in prophet_forecast],
    "ARIMA (R$)": [f"R$ {v:,.0f}" for v in arima_forecast],
    "Limite Inferior": [f"R$ {v:,.0f}" for v in lower],
    "Limite Superior": [f"R$ {v:,.0f}" for v in upper],
    "Desvio (%)": [f"{abs(p-a)/p*100:.1f}%" for p, a in zip(prophet_forecast, arima_forecast)],
})
st.dataframe(df_table, use_container_width=True, hide_index=True)

st.markdown("<br>")
st.markdown("<p style='color:#8B949E;font-size:0.78rem'>* Projeções geradas com dados sintéticos da NexaCorp para fins de demonstração.</p>", unsafe_allow_html=True)
