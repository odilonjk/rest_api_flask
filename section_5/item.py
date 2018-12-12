import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type=float, 
        required=True,
        help='This field cannot be left blank.'
    )

    def get_item(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        
        if row:
            return {'name': row[0], 'price': row[1]}
        return None

    @jwt_required()
    def get(self, name):
        item = Item.get_item(self, name)
        if item:
            return {'item': item}, 200 
        return {'message': 'Item not found.'}, 404

    @jwt_required()
    def post(self, name):
        if Item.get_item(self, name) is not None:
            return {'message': 'An item called {} already exists.'.format(name)}, 400
        data = Item.parser.parse_args()
        new_item = {'name': name, 'price': data['price']}
        items.append(new_item)
        return new_item, 201

    @jwt_required()
    def delete(self, name):
        global items
        if Item.get_item(self, name) is None:
            return {'message': 'There is no item called {}.'.format(name)}, 404
        items = [i for i in items if i['name'] != name]
        return {'message': '{} deleted.'.format(name)}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = Item.get_item(self, name)
        if item is None:
            new_item = {'name': name, 'price': data['price']}
            items.append(new_item)
            return new_item, 201
        item.update(data)
        return item


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': items}