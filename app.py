import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_smorest import Api

from config.jwt_config import JwtConfig
from db import db
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None) -> Flask:
    app = Flask(__name__)
    load_dotenv()

    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = "Stores REST API"
    app.config['API_VERSION'] = "v1"
    app.config['OPENAPI_VERSION'] = "3.0.3"
    app.config['OPENAPI_URL_PREFIX'] = "/"
    app.config['OPENAPI_SWAGGER_UI_PATH'] = "/swagger-ui"
    app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "88663044192488555606631647684698923483721037134868738283367936574020284576353"

    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)
    api = Api(app)

    jwt = JWTManager(app)
    JwtConfig(jwt)

    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
