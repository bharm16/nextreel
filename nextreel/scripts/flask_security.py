import uuid

from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password, RoleMixin, UserMixin
from flask_security.models import fsqla_v3 as fsqla

app = Flask(__name__)

# Your existing database configuration
user_db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'caching_sha2_password',
    'database': 'UserAccounts'
}

# Convert database configuration to SQLAlchemy database URI
db_uri = f"mysql://{user_db_config['user']}:{user_db_config['password']}@{user_db_config['host']}/{user_db_config['database']}"

# Configure your app to use MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some_random_secret_key'
app.config['SECURITY_PASSWORD_SALT'] = 'some_random_salt'
app.config['SECURITY_REGISTERABLE'] = True
# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define roles_users association table
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


# Define User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)  # Add this line
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.fs_uniquifier:
            # Generate a unique fs_uniquifier value
            self.fs_uniquifier = str(uuid.uuid4())


# Define Role model
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Views
# Views
@app.route("/")
@auth_required()
def home():
    return render_template_string("Hello {{ current_user.email }}")


# Now, you can define a function to create a user and role
def create_user():
    # Create a user to test with

    user_datastore.create_user(email="test@me.com", password="password")
    db.session.commit()

    user_datastore.create_role(name="admin", description="Administrator")
    db.session.commit()

    # Assign the admin role to the admin user
    admin_user = user_datastore.get_user("test@me.com")
    admin_role = user_datastore.find_role("admin")
    user_datastore.add_role_to_user(admin_user, admin_role)
    db.session.commit()


# Other imports and Flask app setup

# Define models, Flask-Security setup, and create_user function

if __name__ == "__main__":
    # Push an application context
    with app.app_context():
        create_user()
    app.run(debug=True)
