from flask import Flask, render_template, redirect, session, flash, g
from models import db, connect_db, User, Potty
from forms import SignupForm, LoginForm, BathroomForm
import requests
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///potty_map')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "shhh")

connect_db(app)


@app.before_request
def load_user():
    if "user" in session:
        g.user = User.query.get(session["user"])


@app.route("/")
def get_map_data():
    bathrooms = Potty.query.all()
    if len(bathrooms) < 492:
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


@app.route("/signup", methods=["GET", "POST"])
def user_signup():
    form = SignupForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User.register(full_name, email, username, password)
        db.session.add(user)
        db.session.commit()
        session["user"] = user.id
        return redirect("/home")
    return render_template("signup_form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session["user"] = user.id
            return redirect("/home")
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


@app.route("/profile", methods=["GET", "POST"])
def new_potty():
    user = session['user']
    if user:
        form = BathroomForm()
        if form.validate_on_submit():
            name = form.name.data
            address = form.address.data
            zip_code = form.zip_code.data
            website = form.website.data
            alt_address = address.split(" ")
            input_address = "+".join(alt_address)
            headers = {
                'X-RapidAPI-Key': 'ad9e5957c1msh43164e3dccfa3d0p1ea1f0jsn6c20c5aeb72b',
                'X-RapidAPI-Host': 'google-maps-geocoding.p.rapidapi.com'
            }
            response = requests.get(
                f'https://google-maps-geocoding.p.rapidapi.com/geocode/json?address={input_address}&language=en', headers=headers).json()
            lng = response['results']["geometry"]["location"]["lng"]
            lat = response["results"]["geometry"]["location"]["lat"]
            bathroom = Potty(name=name, address=address, zip_code=zip_code,
                             website=website, longitude=lng, latitude=lat)
            db.session.add(bathroom)
            db.session.commit()
            flash("New Bathroom has been added")
            return redirect("/home")
        else:
            return render_template("new_potty.html", form=form)
    else:
        flash("You are not logged in, please log in before you attempt to add a new bathroom location")
        return redirect("/home")
