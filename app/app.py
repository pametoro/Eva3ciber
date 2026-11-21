from flask import Flask, request
from markupsafe import escape
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Server'] = 'SecureServer'
    return response

@app.route('/')
def index():
    return "<h1>SecureDev App - Versión Mitigada</h1><p>Prueba: <a href='/hello?name=Estudiante'>/hello?name=Estudiante</a></p>"

@app.route('/hello')
def hello():
    raw_name = request.args.get('name', 'Invitado')
    safe_name = escape(raw_name)
    return f"Hello, {safe_name}!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)