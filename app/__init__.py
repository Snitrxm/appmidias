from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_mail import Mail



db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'secret'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = "vitorcontacamp@gmail.com"
    app.config['MAIL_PASSWORD'] = "andrerocha3"
    

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from app import routes
    routes.init_app(app)
    return app