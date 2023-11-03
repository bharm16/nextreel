import uuid

from flask_sqlalchemy import SQLAlchemy

# Initialize your SQLAlchemy instance
# This should be done in your application's setup
db = SQLAlchemy()


# Define the Role model, representing the 'role' table
class Role(db.Model):
    __tablename__ = 'role'

    # Define the columns, their types, and properties
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing primary key
    name = db.Column(db.String(80), unique=True, nullable=True)  # Unique constraint on the 'name' field
    description = db.Column(db.String(255), nullable=True)  # No constraints on 'description'

    # Define the relationship to the User model (defined later)
    # This will not create a new column, but will add a 'users' property to Role objects
    # 'secondary' points to the association table we define next
    users = db.relationship('User', secondary='roles_users', back_populates='roles')


# Define the association table for the many-to-many relationship between Users and Roles
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       # ForeignKey to the User table
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                       # ForeignKey to the Role table
                       )


# Assuming the User model is defined somewhere as:
class User(db.Model):
    __tablename__ = 'user'

    # Assume there are other fields for the User model
    id = db.Column(db.Integer, primary_key=True)

    # New fs_uniquifier field required by Flask-Security
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    # Relationship definition for many-to-many with Role model
    # 'secondary' points to the association table defined above
    roles = db.relationship('Role', secondary='roles_users', back_populates='users')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.fs_uniquifier:
            self.fs_uniquifier = str(uuid.uuid4())  # Ensure uniquifier is set


# Define the UserWatchlist model, representing the 'user_watchlist' table
class UserWatchlist(db.Model):
    __tablename__ = 'user_watchlist'

    # Define the columns, their types, and properties
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)  # Foreign Key to 'user' table
    tconst = db.Column(db.String(255), primary_key=True)  # Part of the composite unique key
    added_at = db.Column(db.DateTime)  # No default specified, will be NULL if not provided
    username = db.Column(db.String(255), nullable=False)  # Not NULL
    poster_url = db.Column(db.String(255), nullable=False)  # Not NULL

    # Define a unique constraint for the combination of user_id and tconst
    __table_args__ = (db.UniqueConstraint('user_id', 'tconst', name='unique_user_movie'),)

    # Define the relationship to the User model
    user = db.relationship('User', backref=db.backref('watchlist', lazy=True))



# Define the UserWatchlistDetail model, representing the 'user_watchlist_detail' table
class UserWatchlistDetail(db.Model):
    __tablename__ = 'user_watchlist_detail'

    # Define the columns, their types, and properties
    id = db.Column(db.Integer, primary_key=True)  # Auto-incrementing primary key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tconst = db.Column(db.String(16), nullable=False)  # Not NULL
    title = db.Column(db.String(255), nullable=False)  # Not NULL
    genres = db.Column(db.String(255))  # Nullable
    directors = db.Column(db.String(255))  # Nullable
    writers = db.Column(db.String(255))  # Nullable
    runtimes = db.Column(db.String(50))  # Nullable
    rating = db.Column(db.Float)  # Nullable
    votes = db.Column(db.Integer)  # Nullable
    poster_url = db.Column(db.String(512))  # Nullable

    # Define the relationship to the User model
    user = db.relationship('User', backref=db.backref('watchlist_details', lazy=True))


class WatchedMovieDetail(db.Model):
    __tablename__ = 'watched_movie_detail'

    # Primary key and auto-incrementing field
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key relating to the 'users' table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Other descriptive fields for the movie details
    tconst = db.Column(db.String(16), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    genres = db.Column(db.String(255))
    directors = db.Column(db.String(255))
    writers = db.Column(db.String(255))
    runtimes = db.Column(db.String(50))
    rating = db.Column(db.Float)
    votes = db.Column(db.Integer)
    poster_url = db.Column(db.String(512))

    # Relationship with the User model
    user = db.relationship('User', backref=db.backref('watched_movie_details', lazy=True))


class WatchedMovies(db.Model):
    __tablename__ = 'watched_movies'

    # Composite primary key consisting of user_id and tconst
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tconst = db.Column(db.String(255), primary_key=True)

    # Additional fields
    watched_at = db.Column(db.DateTime)
    username = db.Column(db.String(255), nullable=False)
    poster_url = db.Column(db.String(255), nullable=False)

    # Unique constraint across user_id and tconst to prevent duplicates
    __table_args__ = (db.UniqueConstraint('user_id', 'tconst', name='unique_user_movie'),)

    # Relationship with the User model
    user = db.relationship('User', backref=db.backref('watched_movies', lazy=True))


# Define the TitleBasics model, representing the 'title.basics' table from the 'imdb' database
class TitleBasics(db.Model):
    __tablename__ = 'title.basics'
    __bind_key__ = 'imdb'  # This is used if you have multiple databases

    # Define the columns, their types, and properties
    tconst = db.Column(db.String(255), primary_key=True)  # Primary key
    titleType = db.Column(db.String(255))  # Index this column if you expect to run queries against it
    primaryTitle = db.Column(db.Text)
    originalTitle = db.Column(db.Text)
    isAdult = db.Column(db.Text)  # This could also be a boolean if 'isAdult' is stored as '0' or '1'
    startYear = db.Column(db.Integer, index=True)  # Index this column
    endYear = db.Column(db.Text)
    runtimeMinutes = db.Column(db.Text)  # This could be an integer if the runtime is always in whole minutes
    genres = db.Column(db.Text)
    plot = db.Column(db.Text)
    poster_url = db.Column(db.String(512))
    language = db.Column(db.Text)

    # Indexes are not reflected in the SQLAlchemy model but they would be used by the database itself.


class TitlePrincipals(db.Model):
    __tablename__ = 'title.principals'
    __bind_key__ = 'imdb'  # Assuming you are using multiple databases

    # Primary key columns
    tconst = db.Column(db.String(255), db.ForeignKey('title.basics.tconst'), primary_key=True)
    nconst = db.Column(db.String(255), primary_key=True)

    # Additional columns
    ordering = db.Column(db.Integer)  # Represents the order of appearance or importance
    category = db.Column(db.Text)  # Text field for the role/category in the title
    job = db.Column(db.Text)  # Text field for the job title if applicable
    characters = db.Column(db.Text)  # Text field for the character(s) played if applicable

    # Index for tconst and nconst for faster search, in SQL it's a composite index
    __table_args__ = (
        db.Index('idx_tconst_nconst', tconst, nconst),
    )


class TitleRatings(db.Model):
    __tablename__ = 'title.ratings'
    __bind_key__ = 'imdb'  # Assuming you are using multiple databases

    # Primary key column
    tconst = db.Column(db.String(255), db.ForeignKey('title.basics.tconst'), primary_key=True)

    # Additional columns for ratings
    averageRating = db.Column(db.Float)  # Average rating for the title
    numVotes = db.Column(db.Integer)  # Number of votes for the title

    # Indexes for tconst, averageRating, and numVotes
    __table_args__ = (
        db.Index('idx_title_ratings_tconst', tconst),
        db.Index('idx_averagerating', averageRating),
        db.Index('idx_numVotes', numVotes),
    )
