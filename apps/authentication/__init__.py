from flask import Blueprint

# Routes associated with blueprint are in a dormant state until the blueprint is registered with an application,
blueprint = Blueprint('authentication_blueprint', __name__, url_prefix='')
