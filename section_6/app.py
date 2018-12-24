from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta

from resources.user import UserRegister, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import User

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True

# JWT
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.secret_key = 'my_secret'

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

jwt = JWTManager(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')


@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    from database import db
    db.init_app(app)
    app.run(port=5000, debug=True)
