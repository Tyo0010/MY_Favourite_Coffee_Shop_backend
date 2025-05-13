from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from flask import Flask

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate(db)

# Create the Flask application instance
flask_app = Flask(__name__)
app = None  # Will be set by create_app

def create_app(flask_instance=None):
    global app
    
    if flask_instance is None:
        flask_instance = flask_app
    
    CORS(flask_instance)
    flask_instance.config.from_object(Config)
    
    # Initialize DB
    db.init_app(flask_instance)
    
    # Initialize migrate
    migrate.init_app(flask_instance, db)
    
    # Register blueprints
    from app.views import blueprint as views_bp
    flask_instance.register_blueprint(views_bp)
    
    from app.errors import blueprint as errors_bp
    flask_instance.register_blueprint(errors_bp)
    
    with flask_instance.app_context():
        db.create_all()
        db.session.commit()
    
    app = flask_instance
    return app