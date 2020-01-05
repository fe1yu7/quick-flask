"""
project setting/config
"""
import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    ACCESS_EXPIRES = datetime.timedelta(days=7)
    REFRESH_EXPIRES = datetime.timedelta(days=30)
    SECRET_KEY = "flask-secret"

    JWT_SECRET_KEY = "flask-jwt-secret"
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_REFRESH_TOKEN_EXPIRES = False
    # JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    MYSQL_CONFIG = None

    SQLALCHEMY_DATABASE_URI = os.environ.get("PRODUCTION_DATABASE_URL") or "mysql+pymysql://{}:{}@{}:{}/{}".format(
        MYSQL_CONFIG["user"],
        MYSQL_CONFIG["password"],
        MYSQL_CONFIG["host"],
        MYSQL_CONFIG["port"],
        MYSQL_CONFIG["db"]
    )


class DevelopmentConfig(BaseConfig):
    """
    development config
    """
    MYSQL_CONFIG = {
        "host": "ip",
        "user": "user",
        "password": "password",
        "port": 3306,
        "db": "db_name"
    }


class ProductionConfig(BaseConfig):
    """
    production config
    """
    MYSQL_CONFIG = {
        "host": "ip",
        "user": "user",
        "password": "password",
        "port": 3306,
        "db": "db_name"
    }


config_mappping = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

config_name = os.environ.get("FLASK_ENV", "development")  # get flask environment
config_class = config_mappping[config_name]
