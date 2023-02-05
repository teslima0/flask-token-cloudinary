from datetime import datetime
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, validate
from.import app,db
import uuid
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
   
    def __repr__(self):
        return '<User %r>' % str(self.id)

   
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    image_url = db.Column(db.String(800))
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('products', lazy=True))
    

    def __init__(self, name, description, price, qty, user, image_url=None):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
        self.user = user
        self.image = image_url

    def __repr__(self):
        return '<Product %r>' % self.id



class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)