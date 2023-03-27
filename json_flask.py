from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/index')
def index():
    data = {
        "alunos": [
            {"nome": "João", "idade": 20},
            {"nome": "Maria", "idade": 22},
            {"nome": "Pedro", "idade": 25}
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run()
