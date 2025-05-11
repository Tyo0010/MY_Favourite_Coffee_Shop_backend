from app import db

class CoffeeShop(db.Model):
    id = db.Column(
        db.Integer, 
        primary_key=True
        )
    name = db.Column(
        db.String(100), 
        nullable=False
        )
    address = db.Column(
        db.String(200), 
        nullable=False
        )
    area = db.Column(
        db.String(100), 
        nullable=False
        )
    opening_hours = db.Column(
        db.String(100), 
        nullable=False
        )
    rating = db.Column(
        db.Float, 
        nullable=True
        )
    
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "area": self.area,
            "opening_hours": self.opening_hours,
            "rating": self.rating
        }