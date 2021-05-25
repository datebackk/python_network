from flask import Flask
from app.config import Config
from flask_wtf.csrf import CSRFProtect
from app.database import db
from app.api.api import api_manager

csrf = CSRFProtect()


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    csrf.init_app(app)

    db.init_app(app)

    with app.app_context():
        from app.blueprints.auth.routes import auth

        app.register_blueprint(auth)
        db.create_all()

        api_manager.init_app(app, flask_sqlalchemy_db=db)

    return app


app = create_app(Config)
