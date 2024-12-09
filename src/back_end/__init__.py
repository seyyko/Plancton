from flask import Flask
import os

def create_app():

    # Initialize the Flask application
    app = Flask(__name__, template_folder='../front_end/templates', static_folder='../front_end/static')

    # Configure the application (you can add your configuration here)
    app.config['SECRET_KEY'] = 'secret_key'
    
    # Import and register the application's routes
    import routes
    app.register_blueprint(routes.bp)

    return app

