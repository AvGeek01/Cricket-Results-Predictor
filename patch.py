import os

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('static/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

with open('static/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

html = html.replace('<link rel="stylesheet" href="/static/style.css">', '<style>\n' + css + '\n</style>')
html = html.replace('<script src="/static/script.js"></script>', '<script>\n' + js + '\n</script>')

with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

import re

# We will replace the home route
new_home_route = """from flask import render_template_string

@app.route('/')
def home():
    return render_template_string(INDEX_HTML)
"""

# use regex to replace the home route including the try/except block
app_py = re.sub(r"@app\.route\('/'\).*?def predict\(\):", new_home_route + "\n@app.route('/predict', methods=['POST'])\ndef predict():", app_py, flags=re.DOTALL)

app_py += '\n\nINDEX_HTML = """' + html + '"""\n'

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)
