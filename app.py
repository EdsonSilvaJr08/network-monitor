from flask import Flask, render_template_string
import requests
import time

app = Flask(__name__)

SITES = [
    {"name": "Google", "url": "https://www.google.com"},
    {"name": "GitHub", "url": "https://www.github.com"},
    {"name": "Cloudflare", "url": "https://www.cloudflare.com"},
    {"name": "Amazon AWS", "url": "https://aws.amazon.com"},
    {"name": "Stack Overflow", "url": "https://stackoverflow.com"},
]

def check_site(site):
    try:
        start = time.time()
        r = requests.get(site["url"], timeout=5)
        elapsed = round((time.time() - start) * 1000)
        return {"name": site["name"], "url": site["url"], "status": "Online", "ms": elapsed}
    except:
        return {"name": site["name"], "url": site["url"], "status": "Offline", "ms": None}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Network Monitor</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #e2e8f0; padding: 40px; }
        h1 { color: #38bdf8; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { background: #1e293b; padding: 12px; text-align: left; color: #94a3b8; }
        td { padding: 12px; border-bottom: 1px solid #1e293b; }
        .online { color: #4ade80; font-weight: bold; }
        .offline { color: #f87171; font-weight: bold; }
        .refresh { margin-top: 20px; color: #64748b; font-size: 13px; }
        a { color: #38bdf8; }
    </style>
</head>
<body>
    <h1>🖥️ Network Monitor</h1>
    <p style="color:#64748b">Monitoramento em tempo real de servidores e sites</p>
    <table>
        <tr><th>Site</th><th>URL</th><th>Status</th><th>Tempo de Resposta</th></tr>
        {% for s in sites %}
        <tr>
            <td>{{ s.name }}</td>
            <td><a href="{{ s.url }}" target="_blank">{{ s.url }}</a></td>
            <td class="{{ 'online' if s.status == 'Online' else 'offline' }}">{{ s.status }}</td>
            <td>{{ s.ms ~ ' ms' if s.ms else '—' }}</td>
        </tr>
        {% endfor %}
    </table>
    <p class="refresh">Atualizado agora. <a href="/">Atualizar</a></p>
</body>
</html>
"""

@app.route("/")
def index():
    results = [check_site(s) for s in SITES]
    return render_template_string(HTML, sites=results)

if __name__ == "__main__":
    app.run(debug=True)