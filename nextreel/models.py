# Define User model
import uuid

from flask_security import RoleMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define roles_users association table
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.fs_uniquifier:
            self.fs_uniquifier = str(uuid.uuid4())  # Ensure uniquifier is set


# Define Role model
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# Define Movie model
class Movie(db.Model):
    __tablename__ = 'title.basics'
    __table_args__ = {'schema': 'imdb'}  # Specify the correct schema here

    tconst = db.Column(db.String(255), primary_key=True)
    titleType = db.Column(db.String(255))
    primaryTitle = db.Column(db.Text)
    originalTitle = db.Column(db.Text)
    isAdult = db.Column(db.Text)
    startYear = db.Column(db.Integer)
    endYear = db.Column(db.Text)
    runtimeMinutes = db.Column(db.Text)
    genres = db.Column(db.Text)
    plot = db.Column(db.Text)
    poster_url = db.Column(db.String(512))
    language = db.Column(db.Text)


# Define UserWatchlist model
class UserWatchlist(db.Model):
    __tablename__ = 'user_watchlist'
    __table_args__ = {'schema': 'UserAccounts'}  # Specify the correct schema here

    user_id = db.Column(db.Integer, db.ForeignKey('UserAccounts.user.id'), primary_key=True)
    tconst = db.Column(db.String(255), db.ForeignKey('imdb.title_basics.tconst'), primary_key=True)

    added_at = db.Column(db.DateTime)
    user = db.relationship('User', backref=db.backref('watchlist', lazy='dynamic'))
    movie = db.relationship('Movie', backref=db.backref('user_watchlist', lazy='dynamic'))
    user = db.relationship('User', back_populates='watchlist')


User.watchlist = db.relationship('UserWatchlist', order_by=UserWatchlist.tconst, back_populates='user')



# Define WatchedMovieDetail model
class WatchedMovieDetail(db.Model):
    __tablename__ = 'watched_movie_detail'
    __table_args__ = {'schema': 'UserAccounts'}  # Specify the correct schema here

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tconst = db.Column(db.String(255), db.ForeignKey('title.basics.tconst'), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    genres = db.Column(db.String(255))
    directors = db.Column(db.String(255))
    writers = db.Column(db.String(255))
    runtimes = db.Column(db.String(50))
    rating = db.Column(db.Float)
    votes = db.Column(db.Integer)
    poster_url = db.Column(db.String(512))

    user = db.relationship('User', backref=db.backref('watched_movie_details', lazy='dynamic'))
    movie = db.relationship('Movie', backref=db.backref('watched_movie_details', lazy='dynamic'))


class WatchedMovies(db.Model):
    __tablename__ = 'watched_movies'
    __table_args__ = {'schema': 'UserAccounts'}  # Specify the correct schema here

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    tconst = db.Column(db.String(255), primary_key=True)
    watched_at = db.Column(db.DateTime)
    username = db.Column(db.String(255), nullable=False)
    poster_url = db.Column(db.String(255), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('user_id', 'tconst', name='unique_user_movie'),
    )


class UserWatchlistDetail(db.Model):
    __tablename__ = 'user_watchlist_detail'
    __table_args__ = {'schema': 'UserAccounts'}  # Specify the correct schema here

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tconst = db.Column(db.String(16), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    genres = db.Column(db.String(255))
    directors = db.Column(db.String(255))
    writers = db.Column(db.String(255))
    runtimes = db.Column(db.String(50))
    rating = db.Column(db.Float)
    votes = db.Column(db.Integer)
    poster_url = db.Column(db.String(512))


class NameBasics(db.Model):
    __tablename__ = 'name_basics'
    __table_args__ = {'schema': 'imdb'}  # Specify the correct schema here

    nconst = db.Column(db.String(255), primary_key=True)
    primaryName = db.Column(db.Text)
    birthYear = db.Column(db.Text)
    deathYear = db.Column(db.Text)
    primaryProfession = db.Column(db.Text)
    knownForTitles = db.Column(db.Text)


class TitleAkas(db.Model):
    __tablename__ = 'title_akas'
    __table_args__ = {'schema': 'imdb'}  # Specify the correct schema here

    # titleId = db.Column(db.String(255), primary_key=True)
    titleId = db.Column(db.String(255), db.ForeignKey('title.basics.tconst'), primary_key=True)  # Added foreign key

    ordering = db.Column(db.Text)
    title = db.Column(db.Text)
    region = db.Column(db.Text)
    language = db.Column(db.Text)
    types = db.Column(db.Text)
    attributes = db.Column(db.Text)
    isOriginalTitle = db.Column(db.Boolean)


class TitleAkasTest(db.Model):  # Assuming this is a test table with similar structure to title.akas
    __tablename__ = 'title_akastest'
    __table_args__ = {'schema': 'imdb'}  # Specify the correct schema here

    titleId = db.Column(db.String(255), primary_key=True)
    ordering = db.Column(db.Text)
    title = db.Column(db.Text)
    region = db.Column(db.Text)
    language = db.Column(db.Text)
    types = db.Column(db.Text)
    attributes = db.Column(db.Text)
    isOriginalTitle = db.Column(db.Boolean)


# class TitleBasics(db.Model):
#     __tablename__ = 'title_basics'
#     __table_args__ = {'schema': 'imdb'}  # Specify the correct schema here
#
#     tconst = db.Column(db.String(255), primary_key=True)
#     titleType = db.Column(db.String(255))
#     primaryTitle = db.Column(db.Text)
#     originalTitle = db.Column(db.Text)
#     isAdult = db.Column(db.Text)
#     startYear = db.Column(db.Integer)
#     endYear = db.Column(db.Text)
#     runtimeMinutes = db.Column(db.Text)
#     genres = db.Column(db.Text)
#     plot = db.Column(db.Text)
#     poster_url = db.Column(db.String(512))
#     language = db.Column(db.Text)


class TitleCrew(db.Model):
    __tablename__ = 'title_crew'
    __table_args__ = {'schema': 'imdb'}  # Specify the correct schema here

    tconst = db.Column(db.String(255), primary_key=True)
    directors = db.Column(db.Text)
    writers = db.Column(db.Text)


class TitleEpisode(db.Model):
    __tablename__ = 'title_episode'
    __table_args__ = {'schema': 'imdb'}  # Specify the correct schema here

    tconst = db.Column(db.String(255), db.ForeignKey('title.basics.tconst'), primary_key=True)  # Added foreign key

    parentTconst = db.Column(db.String(255))
    seasonNumber = db.Column(db.Text)
    episodeNumber = db.Column(db.Text)


class TitlePrincipals(db.Model):
    __tablename__ = 'title_principals'
    __table_args__ = {'schema': 'imdb'}  # Specify the correct schema here

    tconst = db.Column(db.String(255), primary_key=True)
    ordering = db.Column(db.Integer, primary_key=True)
    nconst = db.Column(db.String(255), primary_key=True)
    category = db.Column(db.Text)
    job = db.Column(db.Text)
    characters = db.Column(db.Text)


class TitleRatings(db.Model):
    __tablename__ = 'title_ratings'
    __table_args__ = {'schema': 'imdb'}  # Specify the correct schema here

    tconst = db.Column(db.String(255), primary_key=True)
    averageRating = db.Column(db.Float)
    numVotes = db.Column(db.Integer)
