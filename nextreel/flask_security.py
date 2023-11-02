# flask_security_setup.py
from flask_security import Security, SQLAlchemyUserDatastore
from nextreel.models import db, User, Role

def setup_security(app):
    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)
    return user_datastore
