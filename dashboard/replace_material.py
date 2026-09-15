import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r"st\.markdown\('''<h1 style=.*?>(.*?) Dashboard Ventes</h1>''', unsafe_allow_html=True\)", 'st.title(":material/dashboard: Dashboard Ventes")', content)
content = re.sub(r"st\.markdown\('''<h3 style=.*?>(.*?) Produit le plus vendu</h3>''', unsafe_allow_html=True\)", 'st.subheader(":material/emoji_events: Produit le plus vendu")', content)
content = re.sub(r"st\.markdown\('''<h3 style=.*?>(.*?) Chiffre d\\'affaires mensuel</h3>''', unsafe_allow_html=True\)", 'st.subheader(":material/payments: Chiffre d\'affaires mensuel")', content)
content = re.sub(r"st\.markdown\('''<h3 style=.*?>(.*?) Région la plus performante</h3>''', unsafe_allow_html=True\)", 'st.subheader(":material/public: Région la plus performante")', content)
content = re.sub(r"st\.markdown\('''<h3 style=.*?>(.*?) Clients les plus rentables</h3>''', unsafe_allow_html=True\)", 'st.subheader(":material/group: Clients les plus rentables")', content)
content = re.sub(r"st\.markdown\('''<h3 style=.*?>(.*?) Évolution des ventes</h3>''', unsafe_allow_html=True\)", 'st.subheader(":material/trending_up: Évolution des ventes")', content)
content = re.sub(r"st\.markdown\('''<h3 style=.*?>(.*?) Tendance des ventes</h3>''', unsafe_allow_html=True\)", 'st.subheader(":material/trending_up: Tendance des ventes")', content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
