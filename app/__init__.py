from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import config
from http import HTTPStatus

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name: str = "default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)

    # JWT configuration
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        from .users.models import Blocklist
        return Blocklist.find_by_jti(jwt_payload["jti"])

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            {"msg": "The token has been revoked."},
            HTTPStatus.UNAUTHORIZED,
        )

    from .users.api import blp as UsersBlueprint
    api.register_blueprint(UsersBlueprint)

    return app
