from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)


class Potty(db.Model):
    __tablename__ = "bathrooms"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    address = db.Column(db.Text, nullable=False, unique=True)
    latitude = db.Column(db.Text, nullable=False, unique=True)
    longitude = db.Column(db.Text, nullable=False, unique=True)
