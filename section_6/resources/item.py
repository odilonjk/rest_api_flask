import sqlite3
from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True,
        help='This field cannot be left blank.'
    )

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
            new_item.insert()      
        except:
            return {'message': 'An error occurred inserting the item.'}, 500

        return new_item.json(), 201

    @jwt_required()
    def delete(self, name):
        if ItemModel.find_by_name(name) is None:
            return {'message': 'There is no item called {}.'.format(name)}, 404
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {'message': '{} deleted.'.format(name)}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        new_item = ItemModel(id=None, name=name, price=data['price'])
        item = ItemModel.find_by_name(name)
        if item is None:
            try:
                new_item.insert()      
            except:
                return {'message': 'An error occurred inserting the item.'}, 500
        else:
            try:
                new_item.update()
            except:
                return {'message': 'An error occurred updating the item.'}, 500
        return new_item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[1], 'price': row[2]})
        connection.close()
        return {'items': items}