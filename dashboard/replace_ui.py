
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
if 'import streamlit_shadcn_ui' not in content:
    content = content.replace('import streamlit as st', 'import streamlit as st\nimport streamlit_shadcn_ui as ui')

# Replace metrics in tab1
content = content.replace('''        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            col1.metric("🥇 Produit le plus vendu", best["produit"])
            col2.metric("📦 Quantité vendue", f"{int(best['quantite_totale']):,}".replace(",", " "))
            col3.metric("💵 CA généré", format_ariary(best["chiffre_affaires"]))''',
'''        col1, col2, col3 = st.columns(3)
        with col1:
            ui.metric_card(title="🥇 Produit le plus vendu", content=str(best["produit"]), key="card1_1")
        with col2:
            ui.metric_card(title="📦 Quantité vendue", content=f"{int(best['quantite_totale']):,}".replace(",", " "), key="card1_2")
        with col3:
            ui.metric_card(title="💵 CA généré", content=format_ariary(best["chiffre_affaires"]), key="card1_3")''')

# Replace metrics in tab2
content = content.replace('''        with st.container(border=True):
            col1, col2 = st.columns(2)
            col1.metric("💰 CA du dernier mois", format_ariary(dernier["chiffre_affaires"]), delta=delta_ca)
            col2.metric("📦 Commandes du dernier mois", f"{int(dernier['nb_commandes']):,}".replace(",", " "))''',
'''        col1, col2 = st.columns(2)
        with col1:
            ui.metric_card(title="💰 CA du dernier mois", content=format_ariary(dernier["chiffre_affaires"]), description=delta_ca if delta_ca else "", key="card2_1")
        with col2:
            ui.metric_card(title="📦 Commandes du dernier mois", content=f"{int(dernier['nb_commandes']):,}".replace(",", " "), key="card2_2")''')

# Replace metrics in tab3
content = content.replace('''        with st.container(border=True):
            col1, col2 = st.columns(2)
            col1.metric("🌍 Région la plus performante", best["ville"])
            col2.metric("💵 CA généré", format_ariary(best["chiffre_affaires"]))''',
'''        col1, col2 = st.columns(2)
        with col1:
            ui.metric_card(title="🌍 Région la plus performante", content=str(best["ville"]), key="card3_1")
        with col2:
            ui.metric_card(title="💵 CA généré", content=format_ariary(best["chiffre_affaires"]), key="card3_2")''')

# Replace metrics in tab4
content = content.replace('''        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            col1.metric("🥇 Client le plus rentable", best["client"])
            col2.metric("💵 CA généré", format_ariary(best["chiffre_affaires"]))
            col3.metric("📦 Commandes", f"{int(best['nb_commandes']):,}".replace(",", " "))''',
'''        col1, col2, col3 = st.columns(3)
        with col1:
            ui.metric_card(title="🥇 Client le plus rentable", content=str(best["client"]), key="card4_1")
        with col2:
            ui.metric_card(title="💵 CA généré", content=format_ariary(best["chiffre_affaires"]), key="card4_2")
        with col3:
            ui.metric_card(title="📦 Commandes", content=f"{int(best['nb_commandes']):,}".replace(",", " "), key="card4_3")''')

# Replace metrics in tab5
content = content.replace('''        with st.container(border=True):
            col1, col2 = st.columns(2)
            col1.metric("💵 CA total cumulé", format_ariary(tendance["chiffre_affaires"].sum()))
            col2.metric("📊 CA moyen / jour", format_ariary(tendance["chiffre_affaires"].mean()))''',
'''        col1, col2 = st.columns(2)
        with col1:
            ui.metric_card(title="💵 CA total cumulé", content=format_ariary(tendance["chiffre_affaires"].sum()), key="card5_1")
        with col2:
            ui.metric_card(title="📊 CA moyen / jour", content=format_ariary(tendance["chiffre_affaires"].mean()), key="card5_2")''')


with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
