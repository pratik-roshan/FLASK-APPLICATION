from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from models import ItemModel
from db import db
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint('Items', __name__, url_prefix="/api", description='Operations on items')


@blp.route('/items/<int:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item deleted successfully'}, 200

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema) #response decorator always should be placed deeper
    def put(self, item_data, item_id):
        # Best practice with PUT request is that if item exists, it will be updated
        # If item does not exists, it will be created
        # So at the end of the request, it will return an item -> ie. same if it creates or update and is called idempotent
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item

@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message='An error occurred while inserting the item')
        return item
