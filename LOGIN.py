from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # chave secreta para JWT
api = Api(app)
jwt = JWTManager(app)


from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_bcrypt import generate_password_hash, check_password_hash

parser = reqparse.RequestParser()
parser.add_argument('username', help='Este campo não pode ser deixado em branco', required=True)
parser.add_argument('password', help='Este campo não pode ser deixado em branco', required=True)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        hashed_password = generate_password_hash(data['password'], 10)
        return {'message': 'Usuário criado com sucesso'}, 201

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return {'message': 'Usuário ou senha inválidos'}, 401
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 200


class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {'message': f'Olá, usuário {current_user}!'}

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}

api.add_resource(UserRegistration, '/signup')
api.add_resource(UserLogin, '/login')
api.add_resource(ProtectedResource, '/protected')
api.add_resource(TokenRefresh, '/refresh')

#executando a aplicação
if __name__ == '__main__':
    app.run(debug=True)
