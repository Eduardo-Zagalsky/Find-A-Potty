from app import app
from models import db, User, Potty


db.drop_all()
db.create_all()

user = User(
    full_name='Eddie Z',
    email='eddie@zeta.com',
    username='Eddie',
    password='$2y$12$OKPBu639rqXuhpTAb70Fj.DGmAG/YDD/KQdkqvi6AYG0sWZoStYV.'
)

bathroom = Potty(
    name='My House',
    address='1036 N Dearborn St',
    zip_code='60610',
    longitude='-87.63011829999999',
    latitude='41.9016931',
    website='bjbproperties.com'
)

db.session.add_all([user, bathroom])
db.session.commit()
