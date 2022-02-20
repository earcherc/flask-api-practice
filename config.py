import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # todo: Not even sure if these or values work
    SQLALCHEMY_DATABASE_URI = os.environ[
        "DATABASE_URL"
    ] or "postgresql:///" + os.path.join(basedir, "flask_course")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ["TEST_DATABASE_URI"] or "postgresql:///"


class ProductionConfig(Config):
    # Should be a production db
    SQLALCHEMY_DATABASE_URI = os.environ["PRODUCTION_DATABASE_URI"] or "postgresql:///"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
