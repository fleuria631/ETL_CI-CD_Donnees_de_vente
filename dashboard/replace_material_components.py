
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Tabs
content = content.replace('"Produit le plus vendu"', '":material/emoji_events: Produit le plus vendu"')
content = content.replace('"Chiffre d\'affaires mensuel"', '":material/payments: Chiffre d\'affaires mensuel"')
content = content.replace('"Région la plus performante"', '":material/public: Région la plus performante"')
content = content.replace('"Clients les plus rentables"', '":material/group: Clients les plus rentables"')
content = content.replace('"Tendance des ventes"', '":material/trending_up: Tendance des ventes"')

# Metric Cards
content = content.replace('label="Produit le plus vendu"', 'label=":material/emoji_events: Produit le plus vendu"')
content = content.replace('label="Quantité vendue"', 'label=":material/inventory_2: Quantité vendue"')
content = content.replace('label="CA généré"', 'label=":material/payments: CA généré"')
content = content.replace('label="CA du dernier mois"', 'label=":material/payments: CA du dernier mois"')
content = content.replace('label="Commandes du dernier mois"', 'label=":material/inventory_2: Commandes du dernier mois"')
content = content.replace('label="Région la plus performante"', 'label=":material/public: Région la plus performante"')
content = content.replace('label="Client le plus rentable"', 'label=":material/group: Client le plus rentable"')
content = content.replace('label="Commandes"', 'label=":material/inventory_2: Commandes"')
content = content.replace('label="CA total cumulé"', 'label=":material/payments: CA total cumulé"')
content = content.replace('label="CA moyen / jour"', 'label=":material/monitoring: CA moyen / jour"')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
