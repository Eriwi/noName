from flask import Flask, redirect, Response
from config import Config
from flask_admin import Admin
from flask_admin.contrib import sqla
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException
from flask_mail import Mail

class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))

class ModelView(sqla.ModelView):
    column_display_pk = True

    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())



app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)


admin = Admin(app, name='noName', template_mode='bootstrap3')

db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'
basic_auth = BasicAuth(app)

from server import routes, models

admin.add_view(ModelView(models.Article, db.session))
admin.add_view(ModelView(models.User, db.session))
