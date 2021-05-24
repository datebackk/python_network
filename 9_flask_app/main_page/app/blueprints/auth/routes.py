from app.blueprints.auth import auth
from flask import render_template



@auth.route('/', methods=['GET', 'POST'])
def login():
    return render_template('index.html')