from flask import Flask, request, render_template, redirect, session, flash, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Potty
from forms import SignupForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///potty_map'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup")
def user_signup():
    form = SignupForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User.register(full_name, email, username, password)
        db.session.commit()
        session["user"] = user
        return redirect("/")
    return render_template("signup_form.html", form=form)


@app.route("/login")
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session["user"] = user
            return redirect("/")
        else:
            form.username.errors = ["Incorrect Username/Password"]
    return render_template("login_form.html", form=form)


@app.route("/logout")
def user_logout():
    session.pop("user")
    return redirect("/login")


@app.route("/data")
def data():
    users = User.query.all()
    potties = Potty.query.all()
    return render_template("data.html", users=users, potties=potties)


@app.route("/initiate", methods=["POST"])
def inital_data():
    bathroom = Potty(
        name=request.json["name"],
        address=request.json["address"],
        zip_code=request.json["zip_code"],
        latitude=request.json["latitude"],
        longitude=request.json["longitude"],
        website=request.json["website"])
    db.session.add(bathroom)
    db.session.commit()

    return jsonify(bathroom)
