import plotly.express as px
import streamlit as st
from db import run_query


# Si tu as déjà format_ariary() dans un module utils, remplace la ligne
# ci-dessous par : from utils import format_ariary
def format_ariary(value):
    """Formate un montant en Ariary : espace comme séparateur de milliers, pas de décimales."""
    try:
        return f"{int(round(value)):,}".replace(",", " ") + " Ar"
    except (ValueError, TypeError):
        return "0 Ar"


# ============================================================
# CONFIGURATION GÉNÉRALE & THÈME
# ============================================================
st.set_page_config(page_title="Tableau de bord Ventes", page_icon="📊", layout="wide")

COLOR_SEQ = px.colors.qualitative.Set2
CHART_TEMPLATE = "plotly_white"
ACCENT = "#2563EB"

st.markdown(f"""
    <style>
    /* Cartes de métriques */
    div[data-testid="stMetric"] {{
        background-color: rgba(37, 99, 235, 0.06);
        border: 1px solid rgba(37, 99, 235, 0.15);
        border-radius: 12px;
        padding: 16px 16px 12px 16px;
    }}
    div[data-testid="stMetricValue"] {{
        font-size: 1.55rem;
        font-weight: 600;
    }}
    div[data-testid="stMetricLabel"] {{
        font-size: 0.85rem;
        opacity: 0.75;
    }}

    /* Onglets */
    button[data-baseweb="tab"] {{
        font-size: 1rem;
        font-weight: 600;
        padding: 10px 18px;
    }}
    div[data-baseweb="tab-highlight"] {{
        background-color: {ACCENT};
    }}

    /* Titres de section */
    h2, h3 {{
        font-weight: 700;
    }}

    /* Pills / segmented controls */
    div[data-testid="stPills"] {{
        margin-bottom: 4px;
    }}

    /* Conteneurs avec bordure */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 12px !important;
    }}

    /* Caption "filtre actif" */
    .filtre-actif {{
        display: inline-block;
        background-color: rgba(37, 99, 235, 0.08);
        border: 1px solid rgba(37, 99, 235, 0.2);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.85rem;
        margin-bottom: 8px;
    }}
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard Ventes")
st.caption("Vue d'ensemble des performances commerciales — mise à jour en temps réel depuis l'entrepôt de données")
st.divider()

# Onglets alignés sur les 5 indicateurs de l'architecture DWH
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏆 Produit le plus vendu",
    "💰 Chiffre d'affaires mensuel",
    "🌍 Région la plus performante",
    "👥 Clients les plus rentables",
    "📈 Tendance des ventes",
])

# ============================================================
# INDICATEUR 1 : PRODUIT LE PLUS VENDU
# Fact_Sales + Dim_Product + Dim_Date
# ============================================================
with tab1:
    st.subheader("🏆 Produit le plus vendu")

    categories_df = run_query("""
        SELECT DISTINCT category_name
        FROM analytics_marts.dim_product
        ORDER BY category_name
    """)
    categories_list = ["Toutes"] + categories_df["category_name"].tolist()

    periods_df = run_query("""
        SELECT DISTINCT
            EXTRACT(YEAR FROM dd.full_date)::int AS annee,
            EXTRACT(MONTH FROM dd.full_date)::int AS mois
        FROM analytics_marts.fact_sales fs
        INNER JOIN analytics_marts.dim_date dd ON fs.date_key = dd.date_key
        ORDER BY annee, mois
    """)
    annees_list = ["Toutes"] + sorted(periods_df["annee"].unique().tolist(), reverse=True)

    MOIS_NOMS = {
        1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
        7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
    }

    st.markdown("**Filtrer par catégorie**")
    selected_category = st.pills(
        "Catégorie",
        options=categories_list,
        default="Toutes",
        key="selected_category_pills",
        label_visibility="collapsed",
    )
    selected_category = selected_category or "Toutes"

    col_year, col_month = st.columns(2)
    with col_year:
        selected_year = st.selectbox("📅 Année", options=annees_list, index=0, key="selected_year")
    with col_month:
        if selected_year == "Toutes":
            mois_dispo = ["Tous"] + [MOIS_NOMS[m] for m in sorted(MOIS_NOMS)]
        else:
            mois_dispo_nums = sorted(periods_df.loc[periods_df["annee"] == selected_year, "mois"].unique())
            mois_dispo = ["Tous"] + [MOIS_NOMS[m] for m in mois_dispo_nums]
        selected_month_name = st.selectbox("🗓️ Mois", options=mois_dispo, index=0, key="selected_month")

    filters = []
    if selected_category != "Toutes":
        filters.append(f"dp.category_name = '{selected_category}'")
    if selected_year != "Toutes":
        filters.append(f"EXTRACT(YEAR FROM dd.full_date) = {int(selected_year)}")
    if selected_month_name != "Tous":
        mois_num = [k for k, v in MOIS_NOMS.items() if v == selected_month_name][0]
        filters.append(f"EXTRACT(MONTH FROM dd.full_date) = {mois_num}")

    where_clause = ("WHERE " + " AND ".join(filters)) if filters else ""

    top_products = run_query(f"""
        SELECT
            dp.product_name AS produit,
            dp.category_name AS categorie,
            COUNT(*) AS nb_ventes,
            SUM(fs.quantity) AS quantite_totale,
            SUM(fs.line_total) AS chiffre_affaires
        FROM analytics_marts.fact_sales fs
        INNER JOIN analytics_marts.dim_product dp ON fs.product_key = dp.product_key
        INNER JOIN analytics_marts.dim_date dd ON fs.date_key = dd.date_key
        {where_clause}
        GROUP BY dp.product_key, dp.product_name, dp.category_name
        ORDER BY quantite_totale DESC
        LIMIT 10
    """)

    filtre_txt_parts = []
    if selected_category != "Toutes":
        filtre_txt_parts.append(selected_category)
    if selected_month_name != "Tous":
        filtre_txt_parts.append(selected_month_name)
    if selected_year != "Toutes":
        filtre_txt_parts.append(str(selected_year))
    filtre_txt = " · ".join(filtre_txt_parts) if filtre_txt_parts else "Toutes périodes / catégories confondues"

    st.markdown(f'<span class="filtre-actif">📌 {filtre_txt}</span>', unsafe_allow_html=True)
    st.write("")

    if not top_products.empty:
        best = top_products.iloc[0]
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            col1.metric("🥇 Produit le plus vendu", best["produit"])
            col2.metric("📦 Quantité vendue", f"{int(best['quantite_totale']):,}".replace(",", " "))
            col3.metric("💵 CA généré", format_ariary(best["chiffre_affaires"]))

        st.write("") 
        fig = px.bar(
            top_products, x="produit", y="quantite_totale", color="categorie",
            title=f"Top 10 produits — {filtre_txt}",
            template=CHART_TEMPLATE, color_discrete_sequence=COLOR_SEQ, text="quantite_totale",
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(
            xaxis_title=None, yaxis_title="Quantité vendue", legend_title_text="Catégorie",
            title_font_size=18, margin=dict(t=60, b=20), hoverlabel=dict(bgcolor="white"),
        )
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 Voir le détail en tableau"):
            display_df = top_products.copy()
            display_df["chiffre_affaires"] = display_df["chiffre_affaires"].apply(format_ariary)
            display_df["quantite_totale"] = display_df["quantite_totale"].apply(lambda v: f"{int(v):,}".replace(",", " "))
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucune donnée disponible pour ce filtre.")

    st.divider()
    st.subheader("📈 Évolution des ventes dans le temps")

    granularity = st.pills(
        "Granularité", options=["Mois", "Jour"], default="Mois", key="time_granularity_pills",
    )
    granularity = granularity or "Mois"
    date_trunc_expr = "DATE_TRUNC('month', dd.full_date)" if granularity == "Mois" else "dd.full_date"
    cat_filter_time = f"WHERE dp.category_name = '{selected_category}'" if selected_category != "Toutes" else ""

    sales_over_time = run_query(f"""
        SELECT
            {date_trunc_expr} AS periode,
            dp.product_name AS produit,
            SUM(fs.quantity) AS quantite_totale,
            SUM(fs.line_total) AS chiffre_affaires
        FROM analytics_marts.fact_sales fs
        INNER JOIN analytics_marts.dim_product dp ON fs.product_key = dp.product_key
        INNER JOIN analytics_marts.dim_date dd ON fs.date_key = dd.date_key
        {cat_filter_time}
        GROUP BY periode, dp.product_name
        ORDER BY periode
    """)

    if not sales_over_time.empty:
        idx = sales_over_time.groupby("periode")["quantite_totale"].idxmax()
        top_by_period = sales_over_time.loc[idx].sort_values("periode")

        col_a, col_b = st.columns(2)
        with col_a:
            fig2 = px.bar(
                top_by_period, x="periode", y="quantite_totale", color="produit",
                title=f"Produit dominant par {granularity.lower()}"
                      + (f" — {selected_category}" if selected_category != "Toutes" else ""),
                template=CHART_TEMPLATE, color_discrete_sequence=COLOR_SEQ,
            )
            fig2.update_layout(xaxis_title=None, yaxis_title="Quantité", legend_title_text="Produit", title_font_size=16)
            st.plotly_chart(fig2, use_container_width=True)

        with col_b:
            total_over_time = sales_over_time.groupby("periode", as_index=False).agg(
                quantite_totale=("quantite_totale", "sum"), chiffre_affaires=("chiffre_affaires", "sum")
            )
            fig3 = px.line(
                total_over_time, x="periode", y=["quantite_totale", "chiffre_affaires"],
                title="Évolution globale (quantité & CA)",
                template=CHART_TEMPLATE, color_discrete_sequence=COLOR_SEQ, markers=True,
            )
            fig3.update_layout(xaxis_title=None, yaxis_title=None, legend_title_text=None, title_font_size=16)
            st.plotly_chart(fig3, use_container_width=True)

        with st.expander("📋 Voir le détail en tableau"):
            display_df = top_by_period.copy()
            display_df["chiffre_affaires"] = display_df["chiffre_affaires"].apply(format_ariary)
            display_df["quantite_totale"] = display_df["quantite_totale"].apply(lambda v: f"{int(v):,}".replace(",", " "))
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucune donnée disponible.")

# ============================================================
# INDICATEUR 2 : CHIFFRE D'AFFAIRES MENSUEL
# Fact_Sales + Dim_Date
# ============================================================
with tab2:
    st.subheader("💰 Chiffre d'affaires mensuel")

    ca_mensuel = run_query("""
        SELECT
            DATE_TRUNC('month', dd.full_date)::DATE AS mois,
            SUM(fs.line_total) AS chiffre_affaires,
            COUNT(DISTINCT fs.sales_order_id) AS nb_commandes
        FROM analytics_marts.fact_sales fs
        LEFT JOIN analytics_marts.dim_date dd ON fs.date_key = dd.date_key
        GROUP BY DATE_TRUNC('month', dd.full_date)
        ORDER BY mois
    """)

    if not ca_mensuel.empty:
        dernier = ca_mensuel.iloc[-1]
        prev = ca_mensuel.iloc[-2] if len(ca_mensuel) > 1 else None
        delta_ca = None
        if prev is not None and prev["chiffre_affaires"]:
            delta_ca = f"{(dernier['chiffre_affaires'] / prev['chiffre_affaires'] - 1) * 100:+.1f} %"

        with st.container(border=True):
            col1, col2 = st.columns(2)
            col1.metric("💰 CA du dernier mois", format_ariary(dernier["chiffre_affaires"]), delta=delta_ca)
            col2.metric("📦 Commandes du dernier mois", f"{int(dernier['nb_commandes']):,}".replace(",", " "))

        st.write("")
        fig = px.bar(
            ca_mensuel, x="mois", y="chiffre_affaires", title="Chiffre d'affaires par mois",
            template=CHART_TEMPLATE, color_discrete_sequence=[ACCENT],
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(xaxis_title=None, yaxis_title="Chiffre d'affaires (Ar)", title_font_size=18, margin=dict(t=60, b=20))
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 Voir le détail en tableau"):
            display_df = ca_mensuel.copy()
            display_df["chiffre_affaires"] = display_df["chiffre_affaires"].apply(format_ariary)
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucune donnée disponible.")

# ============================================================
# INDICATEUR 3 : RÉGION LA PLUS PERFORMANTE
# Fact_Sales + Dim_Address
# ============================================================
with tab3:
    st.subheader("🌍 Région la plus performante")

    ca_par_region = run_query("""
        SELECT
            da.city AS ville,
            COUNT(DISTINCT fs.sales_order_id) AS nb_commandes,
            SUM(fs.line_total) AS chiffre_affaires
        FROM analytics_marts.fact_sales fs
        INNER JOIN analytics_marts.dim_address da ON fs.address_key = da.address_key
        GROUP BY da.city
        ORDER BY chiffre_affaires DESC
        LIMIT 10
    """)

    if not ca_par_region.empty:
        best = ca_par_region.iloc[0]
        with st.container(border=True):
            col1, col2 = st.columns(2)
            col1.metric("🌍 Région la plus performante", best["ville"])
            col2.metric("💵 CA généré", format_ariary(best["chiffre_affaires"]))

        st.write("")
        fig = px.bar(
            ca_par_region, x="ville", y="chiffre_affaires", title="Chiffre d'affaires par ville",
            template=CHART_TEMPLATE, color="chiffre_affaires", color_continuous_scale="Blues",
        )
        fig.update_layout(
            xaxis_title=None, yaxis_title="Chiffre d'affaires (Ar)",
            title_font_size=18, margin=dict(t=60, b=20), coloraxis_showscale=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 Voir le détail en tableau"):
            display_df = ca_par_region.copy()
            display_df["chiffre_affaires"] = display_df["chiffre_affaires"].apply(format_ariary)
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    else: 
        st.info("Aucune donnée disponible.")

# ============================================================
# INDICATEUR 4 : CLIENTS LES PLUS RENTABLES
# Fact_Sales + Dim_Customer
# ============================================================
with tab4:
    st.subheader("👥 Clients les plus rentables")  

    top_customers = run_query("""
        SELECT
            dc.first_name || ' ' || dc.last_name AS client,
            dc.customer_type AS type,
            COUNT(DISTINCT fs.sales_order_id) AS nb_commandes,
            SUM(fs.line_total) AS chiffre_affaires
        FROM analytics_marts.fact_sales fs
        INNER JOIN analytics_marts.dim_customer dc ON fs.customer_key = dc.customer_key
        GROUP BY dc.customer_key, dc.first_name, dc.last_name, dc.customer_type
        ORDER BY chiffre_affaires DESC
        LIMIT 10
    """)

    if not top_customers.empty:
        best = top_customers.iloc[0]
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            col1.metric("🥇 Client le plus rentable", best["client"])
            col2.metric("💵 CA généré", format_ariary(best["chiffre_affaires"]))
            col3.metric("📦 Commandes", f"{int(best['nb_commandes']):,}".replace(",", " "))

        st.write("")
        fig = px.bar(
            top_customers, x="client", y="chiffre_affaires", color="type",
            title="Top 10 clients par chiffre d'affaires",
            template=CHART_TEMPLATE, color_discrete_sequence=COLOR_SEQ,
        )
        fig.update_layout(
            xaxis_title=None, yaxis_title="Chiffre d'affaires (Ar)", legend_title_text="Type de client",
            title_font_size=18, margin=dict(t=60, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 Voir le détail en tableau"):
            display_df = top_customers.copy()
            display_df["chiffre_affaires"] = display_df["chiffre_affaires"].apply(format_ariary)
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucune donnée disponible.")

# ============================================================
# INDICATEUR 5 : TENDANCE DES VENTES
# Fact_Sales + Dim_Date
# ============================================================
with tab5:
    st.subheader("📈 Tendance des ventes")

    tendance = run_query("""
        SELECT
            dd.full_date AS jour,
            SUM(fs.line_total) AS chiffre_affaires
        FROM analytics_marts.fact_sales fs
        LEFT JOIN analytics_marts.dim_date dd ON fs.date_key = dd.date_key
        GROUP BY dd.full_date
        ORDER BY jour
    """)

    if not tendance.empty:
        tendance_smooth = tendance.copy()
        tendance_smooth["moyenne_mobile_7j"] = (
            tendance_smooth["chiffre_affaires"].rolling(window=7, min_periods=1).mean()
        )

        with st.container(border=True):
            col1, col2 = st.columns(2)
            col1.metric("💵 CA total cumulé", format_ariary(tendance["chiffre_affaires"].sum()))
            col2.metric("📊 CA moyen / jour", format_ariary(tendance["chiffre_affaires"].mean()))

        st.write("")

        fig = px.line(
            tendance, x="jour", y="chiffre_affaires",
            title="Évolution du chiffre d'affaires dans le temps",
            template=CHART_TEMPLATE, color_discrete_sequence=[ACCENT], markers=False,
        )
        fig.update_layout(xaxis_title=None, yaxis_title="Chiffre d'affaires (Ar)", title_font_size=18, margin=dict(t=60, b=20))
        st.plotly_chart(fig, use_container_width=True)

        fig_smooth = px.line(
            tendance_smooth, x="jour", y="moyenne_mobile_7j",
            title="Tendance lissée (moyenne mobile 7 jours)",
            template=CHART_TEMPLATE, color_discrete_sequence=["#F97316"],
        )
        fig_smooth.update_layout(xaxis_title=None, yaxis_title="Chiffre d'affaires (Ar)", title_font_size=18, margin=dict(t=60, b=20))
        st.plotly_chart(fig_smooth, use_container_width=True)

        with st.expander("📋 Voir le détail en tableau"):
            display_df = tendance.copy()
            display_df["chiffre_affaires"] = display_df["chiffre_affaires"].apply(format_ariary)
            st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("Aucune donnée disponible.")