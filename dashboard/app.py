import streamlit as st
import plotly.express as px
from db import run_query

st.set_page_config(page_title="Dashboard Ventes", layout="wide")
st.title("📊 Dashboard Ventes — esofa_dwh")

# Onglets pour différentes analyses
tab1, tab2, tab3, tab4 = st.tabs(["Vue d'ensemble", "Ventes par client", "Ventes par produit", "Données brutes"])

# ========================
# TAB 1 : VUE D'ENSEMBLE
# ========================
with tab1:
    col1, col2, col3 = st.columns(3)
    
    # KPI : Total des ventes
    total_sales = run_query("SELECT SUM(line_total) as total FROM analytics_marts.fact_sales;")
    col1.metric("💰 Total des ventes", f"${total_sales['total'][0]:,.2f}")
    
    # KPI : Nombre de commandes
    nb_orders = run_query("SELECT COUNT(DISTINCT sales_order_id) as nb FROM analytics_marts.fact_sales;")
    col2.metric("📦 Nombre de commandes", f"{nb_orders['nb'][0]:,}")
    
    # KPI : Nombre de clients
    nb_customers = run_query("SELECT COUNT(DISTINCT customer_key) as nb FROM analytics_marts.fact_sales;")
    col3.metric("👥 Nombre de clients", f"{nb_customers['nb'][0]:,}")
    
    st.divider()
    
    # Graphique : Ventes par mois
    sales_by_month = run_query("""
        SELECT 
            DATE_TRUNC('month', dd.full_date)::DATE as mois,
            SUM(fs.line_total) as total
        FROM analytics_marts.fact_sales fs
        LEFT JOIN analytics_marts.dim_date dd ON fs.date_key = dd.date_key
        GROUP BY DATE_TRUNC('month', dd.full_date)
        ORDER BY mois DESC
        LIMIT 12
    """)
    
    if not sales_by_month.empty:
        fig = px.bar(sales_by_month, x='mois', y='total', title='Ventes par mois (12 derniers mois)')
        st.plotly_chart(fig, use_container_width=True)

# ========================
# TAB 2 : VENTES PAR CLIENT
# ========================
with tab2:
    st.subheader("Top 10 clients par chiffre d'affaires")
    
    top_customers = run_query("""
        SELECT 
            dc.first_name || ' ' || dc.last_name as client,
            dc.customer_type as type,
            COUNT(DISTINCT fs.sales_order_id) as nb_commandes,
            SUM(fs.line_total) as chiffre_affaires
        FROM analytics_marts.fact_sales fs
        INNER JOIN analytics_marts.dim_customer dc ON fs.customer_key = dc.customer_key
        GROUP BY dc.customer_key, dc.first_name, dc.last_name, dc.customer_type
        ORDER BY chiffre_affaires DESC
        LIMIT 10
    """)
    
    st.dataframe(top_customers, use_container_width=True)
    
    # Graphique
    if not top_customers.empty:
        fig = px.bar(top_customers, x='client', y='chiffre_affaires', 
                     title='Top 10 clients', color='type')
        st.plotly_chart(fig, use_container_width=True)

# ========================
# TAB 3 : VENTES PAR PRODUIT
# ========================
with tab3:
    st.subheader("Top 10 produits les plus vendus")
    
    top_products = run_query("""
        SELECT 
            dp.product_name as produit,
            dp.category_name as categorie,
            COUNT(*) as nb_ventes,
            SUM(fs.quantity) as quantite_totale,
            SUM(fs.line_total) as chiffre_affaires
        FROM analytics_marts.fact_sales fs
        INNER JOIN analytics_marts.dim_product dp ON fs.product_key = dp.product_key
        GROUP BY dp.product_key, dp.product_name, dp.category_name
        ORDER BY chiffre_affaires DESC
        LIMIT 10
    """)
    
    st.dataframe(top_products, use_container_width=True)
    
    # Graphique
    if not top_products.empty:
        fig = px.bar(top_products, x='produit', y='chiffre_affaires', 
                     title='Top 10 produits', color='categorie')
        st.plotly_chart(fig, use_container_width=True)

# ========================
# TAB 4 : DONNÉES BRUTES
# ========================
with tab4:
    st.subheader("Données brutes - Fact Sales (10 dernières lignes)")
    df = run_query("""
        SELECT 
            fs.sales_order_id,
            dc.first_name || ' ' || dc.last_name as client,
            dp.product_name as produit,
            fs.quantity,
            fs.unit_price,
            fs.line_total,
            fs.status
        FROM analytics_marts.fact_sales fs
        LEFT JOIN analytics_marts.dim_customer dc ON fs.customer_key = dc.customer_key
        LEFT JOIN analytics_marts.dim_product dp ON fs.product_key = dp.product_key
        ORDER BY fs.sales_order_id DESC
        LIMIT 10
    """)
    st.dataframe(df, use_container_width=True)
