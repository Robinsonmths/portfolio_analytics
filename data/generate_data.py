import pandas as pd
import numpy as np
from faker import Faker
import os

fake = Faker('pt_BR')
np.random.seed(42)
Faker.seed(42)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
N_CUSTOMERS = 2000
N_TRANSACTIONS = 15000

# ── CUSTOMERS ──────────────────────────────────────────────
print("Gerando customers.csv...")
customer_ids = [f"C{str(i).zfill(5)}" for i in range(1, N_CUSTOMERS + 1)]
customers = pd.DataFrame({
    "customer_id": customer_ids,
    "name": [fake.name() for _ in range(N_CUSTOMERS)],
    "age": np.random.randint(18, 70, N_CUSTOMERS),
    "region": np.random.choice(["Sul", "Sudeste", "Norte", "Nordeste", "Centro-Oeste"], N_CUSTOMERS),
    "plan": np.random.choice(["Basic", "Pro", "Enterprise"], N_CUSTOMERS, p=[0.5, 0.35, 0.15]),
    "signup_date": pd.to_datetime(np.random.choice(pd.date_range("2021-01-01", "2023-12-31"), N_CUSTOMERS)),
    "support_tickets": np.random.poisson(2, N_CUSTOMERS),
    "nps_score": np.random.randint(0, 11, N_CUSTOMERS),
    "churned": np.random.choice([0, 1], N_CUSTOMERS, p=[0.77, 0.23]),
})
customers.to_csv(f"{OUTPUT_DIR}/customers.csv", index=False)

# ── TRANSACTIONS ───────────────────────────────────────────
print("Gerando transactions.csv...")
transactions = pd.DataFrame({
    "transaction_id": [f"T{str(i).zfill(6)}" for i in range(1, N_TRANSACTIONS + 1)],
    "customer_id": np.random.choice(customer_ids, N_TRANSACTIONS),
    "date": pd.to_datetime(np.random.choice(pd.date_range("2022-01-01", "2024-06-30"), N_TRANSACTIONS)),
    "amount": np.round(np.random.exponential(250, N_TRANSACTIONS), 2),
    "category": np.random.choice(["Eletrônicos", "Moda", "Casa", "Esporte", "Alimentação"], N_TRANSACTIONS),
    "payment_method": np.random.choice(["Crédito", "Débito", "Pix", "Boleto"], N_TRANSACTIONS),
    "status": np.random.choice(["Concluído", "Cancelado", "Reembolsado"], N_TRANSACTIONS, p=[0.85, 0.10, 0.05]),
})
transactions.to_csv(f"{OUTPUT_DIR}/transactions.csv", index=False)

# ── WAREHOUSES ─────────────────────────────────────────────
print("Gerando warehouses.csv...")
warehouse_ids = [f"WH{str(i).zfill(2)}" for i in range(1, 13)]
warehouses = pd.DataFrame({
    "warehouse_id": warehouse_ids,
    "city": ["São Paulo", "Rio de Janeiro", "Curitiba", "Belo Horizonte", "Salvador",
             "Fortaleza", "Manaus", "Brasília", "Porto Alegre", "Recife", "Goiânia", "Belém"],
    "region": ["Sudeste", "Sudeste", "Sul", "Sudeste", "Nordeste",
                "Nordeste", "Norte", "Centro-Oeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"],
    "capacity": np.random.randint(5000, 20000, 12),
    "utilization_pct": np.round(np.random.uniform(0.55, 0.98, 12), 2),
    "manager": [fake.name() for _ in range(12)],
})
warehouses.to_csv(f"{OUTPUT_DIR}/warehouses.csv", index=False)

# ── LOGISTICS ──────────────────────────────────────────────
print("Gerando logistics.csv...")
n_log = 8000
logistics = pd.DataFrame({
    "shipment_id": [f"SH{str(i).zfill(6)}" for i in range(1, n_log + 1)],
    "warehouse_id": np.random.choice(warehouse_ids, n_log),
    "date": pd.to_datetime(np.random.choice(pd.date_range("2023-01-01", "2024-06-30"), n_log)),
    "destination_region": np.random.choice(["Sul", "Sudeste", "Norte", "Nordeste", "Centro-Oeste"], n_log),
    "delivery_days": np.random.randint(1, 15, n_log),
    "sla_days": np.random.choice([3, 5, 7, 10], n_log),
    "weight_kg": np.round(np.random.exponential(12, n_log), 2),
    "carrier": np.random.choice(["Correios", "Jadlog", "Azul Cargo", "Total Express"], n_log),
    "status": np.random.choice(["Entregue", "Em trânsito", "Atrasado", "Extraviado"], n_log, p=[0.78, 0.12, 0.08, 0.02]),
})
logistics["on_time"] = (logistics["delivery_days"] <= logistics["sla_days"]).astype(int)
logistics.to_csv(f"{OUTPUT_DIR}/logistics.csv", index=False)

# ── QUERY LOGS ─────────────────────────────────────────────
print("Gerando query_logs.csv...")
n_queries = 500
procedures = [f"sp_{fake.word()}_{fake.word()}" for _ in range(50)]
query_logs = pd.DataFrame({
    "query_id": [f"Q{str(i).zfill(4)}" for i in range(1, n_queries + 1)],
    "procedure_name": np.random.choice(procedures, n_queries),
    "execution_date": pd.to_datetime(np.random.choice(pd.date_range("2023-06-01", "2024-06-30"), n_queries)),
    "before_optimization_s": np.round(np.random.uniform(8, 18, n_queries), 2),
    "after_optimization_s": np.round(np.random.uniform(0.4, 1.2, n_queries), 2),
    "table_scans_before": np.random.randint(10, 80, n_queries),
    "table_scans_after": np.random.randint(1, 10, n_queries),
    "rows_processed": np.random.randint(10000, 5000000, n_queries),
    "index_added": np.random.choice([True, False], n_queries, p=[0.65, 0.35]),
})
query_logs.to_csv(f"{OUTPUT_DIR}/query_logs.csv", index=False)

# ── REVENUE MONTHLY ────────────────────────────────────────
print("Gerando revenue_monthly.csv...")
months = pd.date_range("2021-01-01", "2024-06-01", freq="MS")
base = 800000
revenue_monthly = pd.DataFrame({
    "month": months,
    "revenue": np.round(base + np.cumsum(np.random.normal(15000, 40000, len(months))), 2),
    "costs": np.round((base * 0.6) + np.cumsum(np.random.normal(8000, 20000, len(months))), 2),
    "new_customers": np.random.randint(80, 300, len(months)),
    "churned_customers": np.random.randint(20, 90, len(months)),
})
revenue_monthly["profit"] = revenue_monthly["revenue"] - revenue_monthly["costs"]
revenue_monthly.to_csv(f"{OUTPUT_DIR}/revenue_monthly.csv", index=False)

print("\n✅ Todos os datasets gerados com sucesso em data/")
