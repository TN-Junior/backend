from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://desafio-oncase.vercel.app"]}})
    
    db.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    return app
