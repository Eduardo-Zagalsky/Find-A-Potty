from unittest import TestCase
from app import app
from models import db, User, Potty

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_potty_map'
app.config['SQLALCHEMY_ECHO'] = False
app.config['Testing'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class Test_User(TestCase):

    def setUp(self):
        # create table data
        user = User(full_name="John Smith", email="johnsmith@email.com",
                    username="JohnDoe", password="password")
        potty = Potty(name="Grace Place", address="637 S Dearborn St", zip_code="60605", longitude="-87.6291",
                      latitude="41.8735", website="http://gracechicago.org/grace-place/south-loop-campus-ministry/")
        # add data to a session and commit it to the table in database
        db.session.add(user)
        db.session.add(potty)
        db.session.commit()

    def tearDown(self):
        # undo all table data in session not yet commited
        db.session.rollback()
        # delete rows in table
        User.query.delete()
        Potty.query.delete()

    def test_get_info(self):
        # create table data
        user = User(full_name="John Smith", email="johnsmith@email.com",
                    username="JohnDoe", password="password")
        db.session.add(user)
        db.session.commit()
        potty = Potty(name="Grace Place", address="637 S Dearborn St", zip_code="60605", longitude="-87.6291",
                      latitude="41.8735", website="http://gracechicago.org/grace-place/south-loop-campus-ministry/", added_by="admin")
        db.session.add(potty)
        db.session.commit()
        # check user and bathroom data
        self.assertEqual(User.query.all(), {"full_name": "John Smith", "email": "johnsmith@email.com",
                                            "username": "JohnDoe", "password": "password"})

        self.assertEqual(Potty.query.all(), {"name": "Grace Place", "address": "637 S Dearborn St", "zip_code": "60605", "longitude": "-87.6291",
                                             "latitude": "41.8735", "website": "http://gracechicago.org/grace-place/south-loop-campus-ministry/", "added_by": "admin"})

    def test_get_root(self):
        with app.test_client() as client:
            # testing the root route
            resp = client.get("/")
            # root route has redirect so it should have code 302 for redirect
            self.assertEqual(resp.status_code, 302)
            # self.assertEqual(resp.location, "/home")

    def test_post_user(self):
        with app.test_client() as client:
            # testing adding a new user
            resp = client.post("/signup", data={"full_name": "Jane Doe", "email": "janedoe@email.com",
                                                "username": "JaneDoe", "password": "password"})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # test signup for new user
            users = User.query.filter_by(email="janedoe@email.com")
            self.assertEqual(users.json(), {"full_name": "Jane Doe", "email": "janedoe@email.com",
                                     "username": "JaneDoe", "password": "password"})

    def test_post_bathroom(self):
        with app.test_client() as client:
            resp = client.post("/profile", data={"name": "Millennium Park", "address": "201 E Randolph St", "zip_code": "60602", "longitude": "-87.6226",
                                                 "latitude": "41.8826", "website": "https://www.chicago.gov/city/en/depts/dca/supp_info/millennium_park.html"})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # added a new bathroom
            potties = Potty.query.all()
            self.assertEqual(potties, "bathrooms")
