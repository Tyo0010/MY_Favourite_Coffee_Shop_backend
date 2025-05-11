from flask import abort, jsonify, request
from app import db
from app.views import blueprint
from app.models import CoffeeShop, Rating # Import Rating model

@blueprint.route('/add_rating', methods=['POST'])
def add_rating():
    if not request.json:
        abort(400, "Request must be in JSON format")

    # Validate the required fields in the JSON request
    def _validate() -> bool:
        if "coffee_shop_id" not in request.json:
            return False
        if "coffee_rating" not in request.json:
            return False
        if "atmosphere_rating" not in request.json:
            return False
        if "service_rating" not in request.json:
            return False
        if "price_and_value_rating" not in request.json: # Corrected key name from your previous code
            return False
        
        return True
    
    if not _validate():
        abort(400, "One or more required fields are missing")
        
    _coffee_shop_id = request.json["coffee_shop_id"]
    _coffee_rating = request.json["coffee_rating"]
    _atmosphere_rating = request.json["atmosphere_rating"]
    _service_rating = request.json["service_rating"]
    _price_value_rating = request.json["price_and_value_rating"] # Corrected key name
    
    coffee_shop = CoffeeShop.query.get(_coffee_shop_id)
    
    if not coffee_shop:
        abort(404, 'Coffee shop not found')
    
    # Create new rating
    new_rating = Rating(
        coffee_shop_id=_coffee_shop_id,
        coffee_rating=_coffee_rating,
        atmosphere_rating=_atmosphere_rating,
        service_rating=_service_rating,
        price_value_rating=_price_value_rating
    )
    db.session.add(new_rating)
    
    # Recalculate average rating for the coffee shop
    all_ratings = Rating.query.filter_by(coffee_shop_id=_coffee_shop_id).all()
    
    if all_ratings:
        total_ratings_count = len(all_ratings)
        
        # Calculate average for each category
        avg_coffee = sum(r.coffee_rating for r in all_ratings) / total_ratings_count
        avg_atmosphere = sum(r.atmosphere_rating for r in all_ratings) / total_ratings_count
        avg_service = sum(r.service_rating for r in all_ratings) / total_ratings_count
        avg_price_value = sum(r.price_value_rating for r in all_ratings) / total_ratings_count
        
        # Calculate overall average rating for the coffee shop
        # This is a simple average of the category averages. You might want a different weighting.
        overall_avg_rating = (avg_coffee + avg_atmosphere + avg_service + avg_price_value) / 4.0
        coffee_shop.rating = round(overall_avg_rating, 2) #Rounding to 2 decimal places
    else:
        # If this is the first rating, the overall rating is the average of its components
        overall_avg_rating = (_coffee_rating + _atmosphere_rating + _service_rating + _price_value_rating) / 4.0
        coffee_shop.rating = round(overall_avg_rating, 2)

    db.session.commit()

    return jsonify({"message": "Rating added successfully", "coffee_shop_rating": coffee_shop.rating}), 201