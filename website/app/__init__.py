from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import datetime
template_dir = './templates'

app = Flask(__name__, template_folder=template_dir)

#app.config.from_object(Config)
app.config['SECRET_KEY'] = 'jidhfisdlfidsf9d900ds90s0kk32009109dll299s9dd9s0a0l2pl3vmbnmv09'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1/testdb'

db = SQLAlchemy(app)
bc = Bcrypt(app)
loginManager = LoginManager(app)
loginManager.login_view = 'login'
loginManager.login_message_category = 'info'

from app.routes import routes
