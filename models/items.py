from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True) #auto increment
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    # many to one for items table
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    # grab the store object from the store table by matching the store_id defined above
    # back_populates tells that StoreModel will have a field "items" which allows 
    # very easily to access the all the items that belong to that store
    store = db.relationship("StoreModel", back_populates="items")
    
    # secondary="items_tags" -> is the secondary table for many-to-many relationship
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")