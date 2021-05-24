from flask import Flask
from app.config import Config
from flask_wtf.csrf import CSRFProtect
from app.database import db


csrf = CSRFProtect()


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    csrf.init_app(app)

    db.init_app(app)


    with app.app_context():
        from app.blueprints.auth.routes import auth
        # from app.blueprints.main_page.routes import main_page

        app.register_blueprint(auth)
        # app.register_blueprint(main_page)
        db.create_all()

    return app


app = create_app(Config)