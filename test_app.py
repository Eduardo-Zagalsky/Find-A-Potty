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

    def test_get_info(self):
        user = User(full_name="John Smith", email="johnsmith@email.com",
                    username="JohnDoe", password="password")
        db.session.add(user)
        db.session.commit()
        users = User.query.all()
        # check user and bathroom data
        self.assertEqual(users, {"full_name": "John Smith", "email": "johnsmith@email.com",
                                 "username": "JohnDoe", "password": "password"})
        bathroom = Potty(name="Grace Place", address="637 S Dearborn St", zip_code="60605", longitude="-87.6291",
                         latitude="41.8735", website="http://gracechicago.org/grace-place/south-loop-campus-ministry/")
        db.session.add(bathroom)
        db.session.commit()
        bathrooms = Potty.query.all()
        self.assertEqual(bathrooms, {"name": "Grace Place", "address": "637 S Dearborn St", "zip_code": "60605", "longitude": "-87.6291",
                                     "latitude": "41.8735", "website": "http://gracechicago.org/grace-place/south-loop-campus-ministry/"})

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
            self.assertEqual(users, {"full_name": "Jane Doe", "email": "janedoe@email.com",
                                     "username": "JaneDoe", "password": "password"})

    def test_post_bathroom(self):
        with app.test_client() as client:
            resp = client.post("/profile", data={"name": "Millennium Park", "address": "201 E Randolph St", "zip_code": "60602", "longitude": "-87.6226",
                                                 "latitude": "41.8826", "website": "https://www.chicago.gov/city/en/depts/dca/supp_info/millennium_park.html"})
            self.assertEqual(resp.status_code, 200)
            # added a new bathroom
            potties = Potty.query.filter_by(name="Millenium Park")
            self.assertEqual(potties, {"name": "Millennium Park", "address": "201 E Randolph St", "zip_code": "60602", "longitude": "-87.6226",
                             "latitude": "41.8826", "website": "https://www.chicago.gov/city/en/depts/dca/supp_info/millennium_park.html"})
