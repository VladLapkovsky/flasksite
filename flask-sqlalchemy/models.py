from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=True)  # nullable -> not empty
    date = db.Column(db.DateTime, default=datetime.utcnow)

    profile = db.relationship('Profiles', backref='users', uselist=False)  # attr, link to the Profiles attrs
    # To avoid:
    # db.session.query(Users, Profiles).join(Profiles, Users.id == Profiles.user_id).all()

    def __repr__(self):
        return f'<users {self.id}'


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    age = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<profiles {self.id}'
