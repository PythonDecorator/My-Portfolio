from flask_login import current_user, login_user
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.github import github, make_github_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.exc import NoResultFound
from apps.config import Config
from .models import User, db, OAuth


# OAuth is a system that allows two websites to securely share information,
# with well-known OAuth provider like Google or Facebook in order to avoid creating another username and password.
github_blueprint = make_github_blueprint(
    client_id=Config.GITHUB_ID,
    client_secret=Config.GITHUB_SECRET,
    scope='user',
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,),
)


@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):
    info = github.get("/user")

    if info.ok:
        account_info = info.json()
        username = account_info["login"]

        query = User.query.filter_by(oauth_github=username)
        try:
            user = query.one()
            login_user(user)
        except NoResultFound:

            # Save to db
            user = User()
            user.username = '(gh)' + username
            user.oauth_github = username

            # Save current user
            db.session.add(user)
            db.session.commit()

            # login user
            login_user(user)
