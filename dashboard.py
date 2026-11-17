"""Interactive sales dashboard. Run: streamlit run dashboard.py"""
from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st
from src.extract import extract_sales
from src.transform import transform_sales
from src.analytics import summarize_sales

st.set_page_config(page_title="Sales Analytics | ETL Portfolio", page_icon="📊", layout="wide")
DATABASE = Path("outputs/sales.db")
SOURCE = Path("data/sales.csv")


@st.cache_data(show_spinner=False)
def get_data(db_mtime: float | None) -> tuple[pd.DataFrame, str]:
    if db_mtime is not None:
        with sqlite3.connect(DATABASE) as conn:
            frame = pd.read_sql_query("SELECT * FROM sales", conn)
        return frame, "SQLite · dados processados pelo pipeline"
    frame, _ = transform_sales(extract_sales(SOURCE))
    return frame, "CSV · prévia transformada (execute o ETL para gerar o banco)"


mtime = DATABASE.stat().st_mtime if DATABASE.exists() else None
df, origin = get_data(mtime)
df["sale_date"] = pd.to_datetime(df["sale_date"])
df["total_amount"] = pd.to_numeric(df["total_amount"])
df["quantity"] = pd.to_numeric(df["quantity"])

st.title("📊 Sales Analytics Dashboard")
st.caption("Projeto de portfólio · Python + Pandas + SQLite + Streamlit")
st.info(f"Fonte: {origin}")

with st.sidebar:
    st.header("Filtros")
    categories = sorted(df["category"].dropna().unique().tolist())
    selected = st.multiselect("Categorias", categories, default=categories)
    min_date, max_date = df["sale_date"].min().date(), df["sale_date"].max().date()
    period = st.date_input("Período", value=(min_date, max_date), min_value=min_date, max_value=max_date)

filtered = df[df["category"].isin(selected)].copy()
if isinstance(period, (tuple, list)) and len(period) == 2:
    start, end = pd.Timestamp(period[0]), pd.Timestamp(period[1])
    filtered = filtered[filtered["sale_date"].between(start, end)]

if filtered.empty:
    st.warning("Nenhuma venda encontrada para os filtros selecionados.")
    st.stop()

metrics = summarize_sales(filtered)
a, b, c, d = st.columns(4)
a.metric("Faturamento", f"R$ {metrics['revenue']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
b.metric("Vendas", f"{metrics['orders']:,}")
c.metric("Itens vendidos", f"{metrics['units']:,}")
d.metric("Ticket médio", f"R$ {metrics['average_ticket']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

left, right = st.columns(2)
with left:
    st.subheader("Faturamento por dia")
    daily = filtered.assign(day=filtered["sale_date"].dt.date).groupby("day", as_index=True)["total_amount"].sum()
    st.line_chart(daily, y_label="Receita (R$)", x_label="Data")
with right:
    st.subheader("Faturamento por categoria")
    by_category = filtered.groupby("category")["total_amount"].sum().sort_values(ascending=False)
    st.bar_chart(by_category, horizontal=True, x_label="Receita (R$)", y_label="Categoria")

st.subheader("Produtos com maior faturamento")
products = (filtered.groupby("product", as_index=False)
            .agg(quantity=("quantity", "sum"), revenue=("total_amount", "sum"))
            .sort_values("revenue", ascending=False))
st.dataframe(products.rename(columns={"product": "Produto", "quantity": "Unidades", "revenue": "Faturamento (R$)"}),
             use_container_width=True, hide_index=True)

with st.expander("Visualizar vendas filtradas"):
    st.dataframe(filtered.sort_values("sale_date", ascending=False), use_container_width=True, hide_index=True)
st.download_button("⬇️ Exportar vendas filtradas (CSV)",
                   filtered.to_csv(index=False).encode("utf-8-sig"),
                   file_name="filtered_sales.csv", mime="text/csv")
st.caption("Dados sintéticos para fins educacionais. Valores ilustrativos.")
