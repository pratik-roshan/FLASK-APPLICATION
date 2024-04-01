import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import StoreModel
from db import db
from schemas import StoreSchema

blp = Blueprint('Stores', __name__, url_prefix="/api", description='Operations on stores')


@blp.route('/store/<int:store_id>')
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.filter_by(id=store_id).first()

        if store:
            db.session.delete(store)
            db.session.commit()
            return {'message': 'Store deleted successfully'}, 200
        
        else:
            return {'message': 'Store Not Found'}, 404
        
@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message='A store with that name already exists')        
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message='An error occurred while inserting the store')
        return store