import streamlit as st

st.set_page_config(page_title="FAQ | Dúvidas", page_icon="💬", layout="wide")

st.markdown("""
<style>
    .story-box {
        background: #161B22;
        border-left: 3px solid #00D4FF;
        border-radius: 6px;
        padding: 16px 20px;
        margin-bottom: 12px;
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
    .tag {
        background: #21262D;
        color: #00D4FF;
        border-radius: 4px;
        padding: 2px 10px;
        font-size: 0.75rem;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## 💬 Dúvidas Frequentes")
st.markdown("<p style='color:#8B949E;margin-top:-10px'>Perguntas que recrutadores e tech leads costumam fazer sobre os projetos</p>", unsafe_allow_html=True)
st.divider()

faqs = {
    "🔵 Revenue Forecasting Engine": [
        {
            "q": "Por que você escolheu Prophet e não XGBoost para o forecasting?",
            "a": "Prophet é nativo para séries temporais com sazonalidade e tendência — ele lida bem com dados mensais sem precisar de feature engineering manual. XGBoost exigiria criar features de lag, rolling means e codificação de sazonalidade na mão. Para receita mensal com padrão estável, Prophet entrega mais com menos complexidade e é mais fácil de explicar para stakeholders não-técnicos.",
            "tags": ["Modelagem", "Decisão Técnica"]
        },
        {
            "q": "Como você validou que o modelo é confiável?",
            "a": "Usei cross-validation temporal — nunca dados futuros no treino. Separei os últimos 6 meses como holdout e medi MAPE e MAE contra os valores reais. O desvio médio ficou em ±3%, dentro do target de 5% definido pelo time financeiro como aceitável para planejamento trimestral.",
            "tags": ["Validação", "Métricas"]
        },
        {
            "q": "O que você faria diferente se fosse refazer?",
            "a": "Incorporaria variáveis exógenas — inflação, calendário de promoções, sazonalidade de mercado. Um modelo univariado tem teto de precisão quando fatores externos são relevantes. Também automatizaria o retraining mensal com Airflow ou similar para manter o modelo atualizado sem intervenção manual.",
            "tags": ["Melhorias", "MLOps"]
        },
        {
            "q": "Como você comunicou os resultados para o time financeiro?",
            "a": "Criei um dashboard com intervalo de confiança visual e backtesting lado a lado com os valores reais. O ponto chave foi mostrar onde o modelo errou antes de pedir confiança — isso gerou credibilidade. A adoção aconteceu depois de dois meses de acompanhamento comparativo.",
            "tags": ["Comunicação", "Stakeholders"]
        },
    ],
    "🔴 Churn Prediction Model": [
        {
            "q": "Como você chegou em 94% de acurácia?",
            "a": "A acurácia sozinha é enganosa em problemas de churn — as classes são desbalanceadas. Trabalhei com SMOTE para balancear, usei Random Forest com tuning de hiperparâmetros via GridSearchCV e avaliei F1-Score e AUC-ROC como métricas principais. Os 94% refletem o conjunto dessas métricas no set de validação.",
            "tags": ["ML", "Métricas"]
        },
        {
            "q": "Quais foram as features mais importantes no modelo?",
            "a": "NPS score, número de tickets de suporte nos últimos 90 dias e frequência de transações foram os três principais preditores. Faz sentido de negócio — clientes insatisfeitos e com problemas recorrentes têm probabilidade muito maior de churn.",
            "tags": ["Feature Engineering", "Negócio"]
        },
        {
            "q": "Como o modelo foi colocado em produção?",
            "a": "O pipeline foi encapsulado com Scikit-learn Pipeline para garantir que o mesmo pré-processamento do treino fosse aplicado em produção. O score de churn era gerado semanalmente e entregue ao time de Customer Success via dashboard, que priorizava ações de retenção nos clientes com score acima de 0.7.",
            "tags": ["Deploy", "Produção"]
        },
        {
            "q": "Como você mediu o impacto dos 23% de redução no churn?",
            "a": "Comparei a taxa de churn dos clientes que receberam ação de retenção (identificados pelo modelo) versus o trimestre anterior sem modelo. O grupo tratado teve 23% menos cancelamentos. É uma comparação antes/depois — o ideal seria um A/B test formal, o que seria minha recomendação para próximas iterações.",
            "tags": ["Impacto", "Negócio"]
        },
    ],
    "🟡 Supply Chain Dashboard": [
        {
            "q": "Como o dashboard era atualizado em tempo real?",
            "a": "Os dados de logística eram ingeridos via pipeline SQL que rodava a cada 15 minutos no Azure. O Power BI consumia via DirectQuery, então o dashboard refletia o estado atual sem refresh manual. Para os KPIs críticos como atrasos e extraviados, configurei alertas automáticos por e-mail.",
            "tags": ["Arquitetura", "Real-time"]
        },
        {
            "q": "O que significa a redução de 40% no tempo de resposta?",
            "a": "Antes do dashboard, o time de operações identificava problemas por relatórios diários em Excel — a média de detecção de um atraso crítico era de 6 horas. Com o dashboard em tempo real, esse tempo caiu para menos de 1 hora. Medimos antes e depois com logs de tickets de operação.",
            "tags": ["Impacto", "Métricas"]
        },
        {
            "q": "Por que DAX e não Python para as métricas?",
            "a": "O time de operações já usava Power BI e não tinha familiaridade com Python. A decisão foi pragmática — DAX dentro do Power BI mantém a solução acessível para quem vai fazer manutenção. Python seria mais poderoso, mas criaria dependência técnica desnecessária para esse caso.",
            "tags": ["Decisão Técnica", "Negócio"]
        },
    ],
    "🟢 SQL Performance Optimization": [
        {
            "q": "Como você identificou quais queries priorizar?",
            "a": "Usei o pg_stat_statements do PostgreSQL para ranquear as queries por tempo total de execução acumulado — não só as mais lentas individualmente, mas as que mais consumiam recursos no agregado. As top 20 queries respondiam por 80% do tempo total, clássico princípio de Pareto.",
            "tags": ["Diagnóstico", "PostgreSQL"]
        },
        {
            "q": "Como saiu de 12s para 0.8s?",
            "a": "As principais intervenções foram: adição de índices compostos nas colunas mais filtradas, eliminação de table scans via reescrita de subqueries para JOINs, e remoção de funções em cláusulas WHERE que impediam uso de índice. Em alguns casos refatorei cursores para operações set-based, que o PostgreSQL otimiza muito melhor.",
            "tags": ["Otimização", "Técnico"]
        },
        {
            "q": "Como você garantiu que a refatoração não quebrou nada?",
            "a": "Criei um script de validação que rodava as queries antigas e novas em paralelo comparando os resultados linha a linha. Só migrei para produção após 100% de equivalência nos outputs. Além disso, mantive as versões originais comentadas no código por 30 dias como rollback rápido.",
            "tags": ["Qualidade", "Processo"]
        },
    ],
}

for project, questions in faqs.items():
    st.markdown(f"<p class='section-label'>{project}</p>", unsafe_allow_html=True)
    for item in questions:
        with st.expander(f"❓ {item['q']}"):
            tags_html = "".join([f"<span class='tag'>{t}</span>" for t in item['tags']])
            st.markdown(f"{tags_html}<br><br>", unsafe_allow_html=True)
            st.markdown(f"<div class='story-box'>{item['a']}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

st.divider()
st.markdown("<p style='color:#8B949E;font-size:0.78rem;text-align:center'>Tem outra dúvida? Entre em contato via LinkedIn ou e-mail.</p>", unsafe_allow_html=True)
