from app import create_app

# Create application for Lambda
application = create_app()
# This is the WSGI application object that Lambda will call
app = application