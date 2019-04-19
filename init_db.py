from server import db
from server.models import User, Article

db.reflect()
db.drop_all()
db.create_all()