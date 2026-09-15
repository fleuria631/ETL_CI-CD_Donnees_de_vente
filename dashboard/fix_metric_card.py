
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace title= with label= and content= with value= for metric_card
content = content.replace('ui.metric_card(title=', 'ui.metric_card(label=')
content = content.replace(', content=', ', value=')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
