from flask import Blueprint

blueprint = Blueprint('views', __name__)

from app.views import coffee_shops
from app.views import rating
