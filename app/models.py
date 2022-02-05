from app import db
from flask_login import UserMixin
from app import login_manager

@login_manager.user_loader
def current_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(85), nullable=False)
    username = db.Column(db.String(84), nullable=False)
    email = db.Column(db.String(85), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    socialmidias = db.relationship("Socialmidias", backref="user", uselist=False)
    def __str__(self):
        return self.name

class Socialmidias(db.Model):
    __tablename__ = 'socialmidias'
    id = db.Column(db.Integer, primary_key = True)
    username_socialmidias = db.Column(db.String(255), nullable=True)
    facebook = db.Column(db.String(255), nullable=True)
    linkedin = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return self.id 
           


           