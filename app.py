from flask import Flask
from app.views import blueprint
from flask import abort, jsonify, request

@blueprint.after_request
def set_cors(response):
    origin = request.headers.get('Origin')
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Content-Type'] = 'application/json'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@blueprint.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to MY Favourite Coffee Shop API'})

def create_app():  # flask app object
    app = Flask(__name__)
    app.config.from_object('config')  # Configuring from Python files
    
    return app

# Creating the app
app = create_app()  
# Registering the blueprint
app.register_blueprint(blueprint, url_prefix='/meritto')

import os
APP_ENV = os.environ.get('APP_ENV', 'development')

if APP_ENV != 'production':
    app.debug = True

if __name__ == '__main__':  # Running the app
    app.run()