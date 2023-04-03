from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, full_name, email, username, password):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        return cls(full_name=full_name, email=email, username=username, password=hashed_pwd)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.
            Return user if valid; else return False."""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False


class Potty(db.Model):
    __tablename__ = "bathrooms"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    zip_code = db.Column(db.Text, nullable=False)
    longitude = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Text, nullable=False)
    website = db.Column(db.Text)
    added_by = db.Column(db.Text, db.ForeignKey("users.username"))
