from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from config import config

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_name: str):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    jwt.init_app(app)
    api = Api(app)

    from .users.api import blp as UsersBlueprint

    api.register_blueprint(UsersBlueprint)

    if config_name != "testing":
        with app.app_context():
            db.create_all()

    return app
