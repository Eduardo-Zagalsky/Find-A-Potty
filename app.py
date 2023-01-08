from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import SignupForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///potty_map'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup")
def user_signup():
    form = SignupForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User.register(first_name, last_name, email, username, password)
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
