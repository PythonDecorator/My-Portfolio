from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from flask_dance.contrib.github import github
from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import User
from werkzeug.security import generate_password_hash, check_password_hash


# set the current user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Login, Registration and Logout user


@blueprint.route("/github")
def login_github():
    """ GitHub login """
    if not github.authorized:
        return redirect(url_for("github.login"))

    github.get("/user")
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=["GET", "POST"])
def register():
    register_form = CreateAccountForm()
    if request.method == "POST" and register_form.validate_on_submit():

        # check user have been registered
        if User.query.filter_by(email=request.form.get('email')).first():
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('authentication_blueprint.register'))

        # else register user
        new_user = User()
        new_user.name = request.form.get("name")
        new_user.email = request.form.get("email")
        new_user.password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for("home_blueprint.index"))
    return render_template("accounts/register.html", logged_in=current_user.is_authenticated, current_user=current_user,
                           form=register_form)


@blueprint.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "POST" and login_form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        # check email is correct
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('authentication_blueprint.login'))

        # check password correct
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('authentication_blueprint.login'))
        else:
            login_user(user)
            return redirect(url_for('home_blueprint.index'))
    return render_template("accounts/login.html", logged_in=current_user.is_authenticated,
                           current_user=current_user, form=login_form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_blueprint.index'))   # redirects to landing page make sure no login is required


# Errors
# It is a good practice to write the error handlers inside a blueprint this is because if the errorhandler
# decorator is used, the handler will only be invoked for errors that originate in the blueprint.
# To install application-wide error handlers, the app_errorhandler must be used instead.

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error():
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error():
    return render_template('home/page-500.html'), 500
