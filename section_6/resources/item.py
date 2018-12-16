from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank.')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found.'}, 404

    @jwt_required()
    def post(self, name):
        user = current_identity
        print('{} is trying to create a new item called {}.'.format(user.username, name))
        if ItemModel.find_by_name(name) is not None:
            return {'message': 'An item called {} already exists.'.format(name)}, 400
        data = Item.parser.parse_args()
        new_item = ItemModel(id=None, name=name, price=data['price'])

        try:
            new_item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500

        return new_item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': '{} deleted.'.format(name)}
        return {'message': 'There is no item called {}.'.format(name)}, 404

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(None, name, data['price'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        items = ItemModel.find_all()
        return [item.json() for item in items]