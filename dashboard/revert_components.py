import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# I want to restore the icons in st.title and st.subheader
# And remove them from the UI components

# First, remove them everywhere:
content = re.sub(r':material/[a-z0-9_]+:\s*', '', content)

# Then, add them back ONLY in st.title and st.subheader
content = content.replace('st.title("Dashboard Ventes")', 'st.title(":material/dashboard: Dashboard Ventes")')
content = content.replace('st.subheader("Produit le plus vendu")', 'st.subheader(":material/emoji_events: Produit le plus vendu")')
content = content.replace('st.subheader("Chiffre d\'affaires mensuel")', 'st.subheader(":material/payments: Chiffre d\'affaires mensuel")')
content = content.replace('st.subheader("Région la plus performante")', 'st.subheader(":material/public: Région la plus performante")')
content = content.replace('st.subheader("Clients les plus rentables")', 'st.subheader(":material/group: Clients les plus rentables")')
content = content.replace('st.subheader("Évolution des ventes")', 'st.subheader(":material/trending_up: Évolution des ventes")')
content = content.replace('st.subheader("Tendance des ventes")', 'st.subheader(":material/trending_up: Tendance des ventes")')


with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
