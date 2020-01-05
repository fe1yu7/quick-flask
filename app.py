from flask import Flask

from config import config_class
from ext import db, jwt, ma, csrf_protect
from resource.user.urls import blueprint as user_blueprint
from resource.auth.urls import blueprint as auth_blueprint


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)

    configure_extensions(flask_app)
    register_blueprints(flask_app)

    return flask_app


def configure_extensions(flask_app):
    """配置扩展工具"""
    db.init_app(flask_app)
    jwt.init_app(flask_app)
    # csrf_protect.init_app(flask_app)


def register_blueprints(flask_app):
    flask_app.register_blueprint(user_blueprint, url_prefix="/user")
    flask_app.register_blueprint(auth_blueprint, url_prefix="/auth")


app = create_app()

