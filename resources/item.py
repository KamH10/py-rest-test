
from flask_restful import Resource, reqparse        # **NOTE**
from flask_jwt import jwt_required                  # **NOTE**  s07e10-added
from models.item import ItemModel

class Item(Resource):                               # **NOTE**
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")

    @jwt_required()                                     # **NOTE** VIP (POS1) s07e10-added
    def get(self, name):                                # **NOTE** get()
        print("==> Item.get()")                         # fDBG
        item = ItemModel.find_by_name(name)             # **NOTE**
        if item:
            return item.json()                          # **NOTE**
        return {'message': 'Item not found'}, 404       # **NOTE**

    def post(self, name):
        print("==> Item.post()")  # fDBG
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        # **NOTE** extract some values from json payload of the request
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)      # **NOTE**

        try:
            item.save_to_db()               # **NOTE**
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        print("==> Item.delete()")  # fDBG
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()           # **NOTE**

        return {'message': 'Item deleted'}

    def put(self, name):
        print("==> Item.put()")  # fDBG
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)      # **NOTE**
        else:
            item.price = data['price']          # **NOTE**

        item.save_to_db()

        return item.json()                      # **NOTE**


class ItemList(Resource):
    def get(self):
        # return list of items
        return {'items': [x.json() for x in ItemModel.query.all()]}
