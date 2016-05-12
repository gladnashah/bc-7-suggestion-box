import os
from flask.ext.login import LoginManager
from config import basedir
from flask import Flask
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown



app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
bootstrap = Bootstrap(app)
moment = Moment(app)
pagedown = PageDown(app)

@app.context_processor
def inject_permissions():
	return dict(Permission=Permission)

from app import views, models