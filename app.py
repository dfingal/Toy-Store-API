from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate, identity
from user import UserRegister
from pet import Pet, PetList
from toy import Toy, ToyList


app = Flask(__name__)
app.secret_key = 'password'
api = Api(app)

jwt = JWT(app, authenticate, identity)

#items = []

# class Item(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('price', type=float, required=True, help="Do not leave blank!")

#     @jwt_required()
#     def get(self, name):
#         return {'item': next(filter(lambda x: x['name'] == name, items), None)}
    
#     #@jwt_required()
#     def post(self, name):
#         if next(filter(lambda x: x['name'] == name, items), None) is not None:
#             return {'message': "An item with the name '{}' already exisits.". format(name)}

#         data = Item.parser.parse_args()

#         item = {'name': name, 'price': data['price']}
#         items.append(item)
#         return item

#     @jwt_required()
#     def delete(self, name):
#         global items
#         items = list(filter(lambda x: x['name'] == name, items), None)
#         return {'message': 'Item deleted'}

#     #@jwt_required()
#     def put(self, name):
#         data = Item.parser.parse_args()
#         item = next(filter(lambda x: x['name'] == name, items), None)
#         if item is None:
#             item = {'name': name, 'price': data['price']}
#             items.append(item)
#         else:
#             item.update(data)
#         return item

# class ItemList(Resource):
#     @jwt_required()
#     def get(self):
#         return {'items': items}

api.add_resource(Pet, '/pet/<string:name>')
api.add_resource(PetList, '/pets')
api.add_resource(Toy, '/toy/<string:name>')
api.add_resource(ToyList, '/toys')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True)