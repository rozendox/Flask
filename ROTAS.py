import requests

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/rota', methods=['GET'])
def rota():
    # Obter parâmetros da requisição
    origem = request.args.get('origem')
    destino = request.args.get('destino')

    # Obter informações da rota a partir da API do Google Maps
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={origem}&destination={destino}&key=SUA_CHAVE_AQUI'
    response = requests.get(url)
    dados = response.json()

    # Analisar informações da rota e retornar resultado
    if dados['status'] == 'OK':
        rota = dados['routes'][0]
        distancia = rota['legs'][0]['distance']['text']
        duracao = rota['legs'][0]['duration']['text']
        passos = [step['html_instructions'] for step in rota['legs'][0]['steps']]
        resultado = {
            'distancia': distancia,
            'duracao': duracao,
            'passos': passos
        }
        return jsonify(resultado)
    else:
        return jsonify({'erro': 'Não foi possível obter informações da rota'})

if __name__ == '__main__':
    app.run(debug=True)
