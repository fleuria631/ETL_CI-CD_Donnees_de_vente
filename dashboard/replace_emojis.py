
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace emojis in ui.tabs and string variables
content = content.replace("🏆 Produit le plus vendu", "Produit le plus vendu")
content = content.replace("💰 Chiffre d'affaires mensuel", "Chiffre d'affaires mensuel")
content = content.replace("🌍 Région la plus performante", "Région la plus performante")
content = content.replace("👥 Clients les plus rentables", "Clients les plus rentables")
content = content.replace("📈 Tendance des ventes", "Tendance des ventes")

# Metric cards
content = content.replace("🥇 Produit le plus vendu", "Produit le plus vendu")
content = content.replace("📦 Quantité vendue", "Quantité vendue")
content = content.replace("💵 CA généré", "CA généré")
content = content.replace("💰 CA du dernier mois", "CA du dernier mois")
content = content.replace("📦 Commandes du dernier mois", "Commandes du dernier mois")
content = content.replace("🌍 Région la plus performante", "Région la plus performante")
content = content.replace("🥇 Client le plus rentable", "Client le plus rentable")
content = content.replace("📦 Commandes", "Commandes")
content = content.replace("💵 CA total cumulé", "CA total cumulé")
content = content.replace("📊 CA moyen / jour", "CA moyen / jour")

# Select boxes
content = content.replace("📅 Année", "Année")
content = content.replace("🗓️ Mois", "Mois")

# Badges
content = content.replace("📌 Filtre actif : ", "Filtre actif : ")

# Expanders
content = content.replace("📋 Voir le détail en tableau", "Voir le détail en tableau")

# Titles (Replace with SVG)
dashboard_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-layout-dashboard" style="vertical-align: middle; margin-right: 8px;"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>'''
content = content.replace('st.title("📊 Dashboard Ventes")', f'st.markdown(\'\'\'<h1 style="display: flex; align-items: center;">{dashboard_svg} Dashboard Ventes</h1>\'\'\', unsafe_allow_html=True)')

trophy_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-trophy" style="vertical-align: middle; margin-right: 8px;"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>'''
content = content.replace('st.subheader("🏆 Produit le plus vendu")', f'st.markdown(\'\'\'<h3 style="display: flex; align-items: center; margin-top: 1rem;">{trophy_svg} Produit le plus vendu</h3>\'\'\', unsafe_allow_html=True)')

dollar_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-circle-dollar-sign" style="vertical-align: middle; margin-right: 8px;"><circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8"/><path d="M12 18V6"/></svg>'''
content = content.replace('st.subheader("💰 Chiffre d\'affaires mensuel")', f'st.markdown(\'\'\'<h3 style="display: flex; align-items: center; margin-top: 1rem;">{dollar_svg} Chiffre d\\\'affaires mensuel</h3>\'\'\', unsafe_allow_html=True)')

globe_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-globe" style="vertical-align: middle; margin-right: 8px;"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>'''
content = content.replace('st.subheader("🌍 Région la plus performante")', f'st.markdown(\'\'\'<h3 style="display: flex; align-items: center; margin-top: 1rem;">{globe_svg} Région la plus performante</h3>\'\'\', unsafe_allow_html=True)')

users_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-users" style="vertical-align: middle; margin-right: 8px;"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'''
content = content.replace('st.subheader("👥 Clients les plus rentables")', f'st.markdown(\'\'\'<h3 style="display: flex; align-items: center; margin-top: 1rem;">{users_svg} Clients les plus rentables</h3>\'\'\', unsafe_allow_html=True)')

trend_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-trending-up" style="vertical-align: middle; margin-right: 8px;"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>'''
content = content.replace('st.subheader("📈 Évolution des ventes")', f'st.markdown(\'\'\'<h3 style="display: flex; align-items: center; margin-top: 1rem;">{trend_svg} Évolution des ventes</h3>\'\'\', unsafe_allow_html=True)')
content = content.replace('st.subheader("📈 Tendance des ventes")', f'st.markdown(\'\'\'<h3 style="display: flex; align-items: center; margin-top: 1rem;">{trend_svg} Tendance des ventes</h3>\'\'\', unsafe_allow_html=True)')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
