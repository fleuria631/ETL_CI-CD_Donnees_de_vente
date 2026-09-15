
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace st.dataframe with ui.table where appropriate
content = content.replace('st.dataframe(display_df, use_container_width=True, hide_index=True)', 'ui.table(data=display_df)')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
