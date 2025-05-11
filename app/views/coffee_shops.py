from flask import abort, jsonify, request
from app import db
from app.views import blueprint
from app.models import CoffeeShop

@blueprint.route('/coffee_shops', methods=['GET'])
def get_coffee_shops():
    """
    Get all coffee shops
    """
    coffee_shops = CoffeeShop.query.all()
    return jsonify([coffee_shop.serialize() for coffee_shop in coffee_shops]), 200

@blueprint.route('/new_coffee_shop', methods=['POST'])
def new_coffee_shop():
    if not request.json:
        abort(400, "Request must be in JSON format")

    # Validate the required fields in the JSON request
    def _validate() -> bool:
        if "name" not in request.json:
            return False
        if "address" not in request.json:
            return False
        if "area" not in request.json:
            return False
        if "opening_hours" not in request.json:
            return False
        
        return True
    
    if not _validate():
        abort(400, "One or more required fields are missing")
        
    _name = request.json["name"]
    _address = request.json("address")
    _area = request.json("area")
    _opening_hours = request.json("opening_hours")
    
    exist_branch = CoffeeShop.query.filter_by(address=_address).first()
    
    if exist_branch:
        abort(404, 'User already exists')
        
    new_coffee_shop = CoffeeShop(
        name=_name,
        address=_address,
        area=_area,
        opening_hours=_opening_hours
    )
    db.session.add(new_coffee_shop)
    db.session.commit()
    return jsonify(new_coffee_shop.serialize()), 201

@blueprint.route('/coffee_shops/<int:coffee_shop_id>', methods=['DELETE'])
def delete_coffee_shop(coffee_shop_id):
    """
    Delete a coffee shop
    """
    coffee_shop = CoffeeShop.query.get(coffee_shop_id)
    if not coffee_shop:
        abort(404, "Coffee shop not found")
    
    db.session.delete(coffee_shop)
    db.session.commit()
    return jsonify({"message": "Coffee shop deleted"}), 200

@blueprint.route('/update_shop/<int:id>', methods=['PUT'])
def update_coffee_shop(id):
    """
    Update a coffee shop
    """
    if not request.json:
        abort(400, "Request must be in JSON format")

    # Validate the required fields in the JSON request
    
    coffee_shop = CoffeeShop.query.get(id)
    if not coffee_shop:
        abort(404, "Coffee shop not found")
    data = request.json()
    
    if 'name' in data:
        coffee_shop.name = data['name']
    if 'address' in data:
        coffee_shop.address = data['address']
    if 'area' in data:
        coffee_shop.area = data['area']
    if 'opening_hours' in data:
        coffee_shop.opening_hours = data['opening_hours']
    
    db.session.commit()
    
    return jsonify(coffee_shop.serialize()), 200