from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
LoginManager.login_view = 'login'


db = SQLAlchemy(app)
app.app_context().push()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

