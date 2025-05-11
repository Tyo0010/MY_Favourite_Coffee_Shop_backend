from app import db
from app.models import CoffeeShop

class Rating(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
        )
    coffee_shop_id = db.Column(
        db.Integer, 
        db.ForeignKey('coffee_shop.id'), 
        nullable=False
        )
    coffee_rating = db.Column(
        db.Integer, 
        nullable=False
        )
    atmosphere_rating = db.Column(
        db.Integer, 
        nullable=False
        )
    service_rating = db.Column(
        db.Integer, 
        nullable=False
        )
    price_value_rating = db.Column(
        db.Integer, 
        nullable=False
        )
    
    coffee_shop = db.relationship(
        CoffeeShop, 
        backref='ratings'
    )
    
    def serialize(self):
        return {
            "id": self.id,
            "coffee_shop_id": self.coffee_shop_id,
            "coffee_rating": self.coffee_rating,
            "atmosphere_rating": self.atmosphere_rating,
            "service_rating": self.service_rating,
            "price_value_rating": self.price_value_rating
        }