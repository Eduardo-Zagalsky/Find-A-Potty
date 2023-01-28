from flask import Flask, request, render_template, redirect, session, flash, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Potty
from forms import SignupForm, LoginForm
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///potty_map'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.before_request
def load_user():
    if "user" in session:
        g.user = User.query.get(session["user"])


@app.route("/")
def get_map_data():
    response = requests.get(
        "https://www.arcgis.com/sharing/rest/content/items/cc11a895caa848a886014c75835d2d91/data?f=json").json()
    result = response['operationalLayers'][0]["featureCollection"]["layers"][0]["featureSet"]["features"]
    for res in result:
        bathroom = res["attributes"]
        name = bathroom['building_name']
        address = bathroom['address']
        zip_code = bathroom['zip']
        latitude = bathroom['latitude']
        longitude = bathroom['longitude']
        website = bathroom['site_link']
        potty = Potty(name=name, address=address, zip_code=zip_code,
                      longitude=longitude, latitude=latitude, website=website)
        db.session.add(potty)
        db.session.commit()
    return redirect("/home")


@app.route("/home")
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
