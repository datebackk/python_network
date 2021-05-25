from flask import Blueprint
from flask_login import LoginManager
from app.database import db
from app.database.models.user import User


auth = Blueprint('auth', __name__, template_folder='templates/auth', static_folder='static/auth')

login_manager = LoginManager()

login_manager.login_view = "auth.login"
login_manager.login_message = u"Пожалуйста авторизуйтесь чтобы получить доступ к этой странице"

@auth.record_once
def on_load(state):
    login_manager.init_app(state.app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)