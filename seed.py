from app import app
from models import db, User, Potty


db.drop_all()
db.create_all()

user = User(
    name='Eddie Z',
    email='eddie@zeta.com',
    username='Eddie',
    password='$2b$12$8ZyEYe2PtS9zQvnmKW03EOJH/k3gDJMVo14vSXWHH5tXwcJrxq4VO'
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
