from flask_login import UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from apps import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String)

    oauth_github = db.Column(db.String(100), nullable=True)

    def to_dict(self) -> dict:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class ContactUs(db.Model):
    __tablename__ = "contact_us"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default="datetime.utcnow")  # will be added by default
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    message = db.Column(db.String(250), nullable=False)


class Portfolio(db.Model):
    __tablename__ = "portfolios"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    github_url = db.Column(db.String, nullable=False)
    final_project = db.Column(db.String, nullable=False)
    download = db.Column(db.String, nullable=False)
    client = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="cascade"), nullable=False)
    user = db.relationship(User)
