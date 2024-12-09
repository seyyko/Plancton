from flask import Flask
import os

def create_app():

    # Initialize the Flask application
    app = Flask(__name__, template_folder='../front_end/templates', static_folder='../front_end/static')

    # Configure the application (you can add your configuration here)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_key')
    # you can set you own secret key (e.g. in powershell)
    # $env:SECRET_KEY = "my_secret_key"
    # after the manipulation, uncomment below to see if it was succeessful!
    # print("⚠️  IMPORTANT :", os.getenv('SECRET_KEY', 'default_key'))
    
    # Import and register the application's routes
    import routes
    app.register_blueprint(routes.bp)

    return app

