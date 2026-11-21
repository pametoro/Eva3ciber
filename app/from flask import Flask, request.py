from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>SecureDev App - Evaluación 3</h1><p>Prueba: <a href='/hello?name=Estudiante'>/hello?name=Estudiante</a></p>"

@app.route('/hello')
def hello():
    name = request.args.get('name')
    return f"Hello, {name}!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)