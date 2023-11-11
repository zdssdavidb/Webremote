from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask import Flask

app = Flask(__name__,
        static_folder='../static/',
        template_folder='../templates/')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "3GShz7"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

# write_log("Configured database")

class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)

db.init_app(app)

