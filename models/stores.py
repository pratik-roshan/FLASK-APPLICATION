from db import db

"""
CASCADE:
- when store deleted, deletes all the items in that store

One-2-Many relationship between store and tags
"""



class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    # back_populates "store" tells that ItemModel will have a field "store"
    # so basically thses defines the two end of the relationship
    # i.e "items" for store table and "store" for item table
    # item has store and store has items
    # One to many
    # lazy="dynamic" means that items will not be loaded from db until we tell it to
    # i.e it will not gonna be prefetched 
    # Delete all the items that are in the store, when store is deleted
    items = db.relationship(
        "ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete"
    )

    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")