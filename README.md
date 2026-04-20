# 📊 Robinson Matheus — Data Analytics Portfolio

> **Analista de Dados | Decision Intelligence**
> Portfolio interativo construído com Python e Streamlit, demonstrando projetos de análise de dados, machine learning e otimização de sistemas.

---

## 🚀 Como Rodar

\`\`\`bash
git clone https://github.com/seu-usuario/portfolio_analytics.git
cd portfolio_analytics
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python data/generate_data.py
streamlit run app.py
\`\`\`

---

## 🗂️ Projetos

### 🔴 Churn Prediction Model
**Problema:** A NexaCorp perdia clientes sem conseguir antecipar o movimento.

**Solução:** Pipeline de Machine Learning com Random Forest para identificar clientes em risco antes do cancelamento.

**Stack:** Python · Scikit-learn · Pandas · Plotly

**Resultados:**
- 94% de acurácia (F1: 0.91 · AUC-ROC: 0.96)
- Redução de 23% no churn no trimestre seguinte
- Top features: NPS Score, Tickets de Suporte, Plano

---

### 🟡 Supply Chain Dashboard
**Problema:** Time de operações gerenciava 12 armazéns via relatórios diários em Excel.

**Solução:** Dashboard em tempo real centralizando todos os indicadores logísticos com alertas automáticos para SLA em risco.

**Stack:** SQL · Plotly · DAX · Azure

**Resultados:**
- Redução de 40% no tempo médio de resposta a incidentes
- Monitoramento em tempo real de 12 armazéns

---

### 🟢 SQL Performance Optimization
**Problema:** Stored procedures críticas levavam até 18 segundos para executar.

**Solução:** Diagnóstico via pg_stat_statements, refatoração de subqueries para JOINs e criação de índices compostos.

**Stack:** PostgreSQL · Query Tuning · Indexing

**Resultados:**
- Redução de 12s para 0.8s de tempo médio de execução
- Ganho de 15x de performance em 200+ stored procedures

---

### 🔵 Revenue Forecasting Engine
**Problema:** Decisões de budget eram tomadas sem visibilidade de receita futura.

**Solução:** Engine de forecasting com Prophet e ARIMA para projeções de 6 meses com simulação de cenários.

**Stack:** Python · Prophet · ARIMA · Plotly

**Resultados:**
- Desvio médio de ±3% em projeções de 6 meses
- Adotado pelo time financeiro como referência de planejamento trimestral

---

## 🛠️ Stack Técnica

| Categoria | Tecnologias |
|---|---|
| Linguagens | Python · SQL |
| ML e Stats | Scikit-learn · Prophet · ARIMA · Pandas · NumPy |
| Visualização | Plotly · Streamlit |
| Banco de Dados | PostgreSQL |
| BI | Power BI · DAX |
| Ambiente | Linux · Git · Jupyter |

---

## 📁 Estrutura do Projeto

\`\`\`
portfolio_analytics/
├── app.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── data/
│   ├── generate_data.py
│   ├── customers.csv
│   ├── transactions.csv
│   ├── warehouses.csv
│   ├── logistics.csv
│   ├── query_logs.csv
│   └── revenue_monthly.csv
└── pages/
    ├── 01_churn.py
    ├── 02_supply_chain.py
    ├── 03_sql_performance.py
    ├── 04_revenue_forecast.py
    └── 05_faq.py
\`\`\`

---

## ⚠️ Nota sobre os Dados

Todos os projetos utilizam dados **sintéticos gerados via Faker e NumPy**, representando uma empresa fictícia chamada **NexaCorp**. As metodologias, decisões técnicas e resultados são baseados em práticas reais de mercado.

Os dados reais não estão disponíveis por razões de confidencialidade de clientes.

---

## 📬 Contato

**Robinson Matheus** — Data Analyst · Decision Intelligence

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/seu-perfil)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:seu@email.com)
