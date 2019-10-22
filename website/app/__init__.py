from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import Config
template_dir = './templates'

db = SQLAlchemy()
bc = Bcrypt()
loginManager = LoginManager()
app = Flask(__name__, template_folder=template_dir)

app.config.from_object(Config)

db.init_app(app)
bc.init_app(app)
loginManager.init_app(app)

from app.routes import routes, api
