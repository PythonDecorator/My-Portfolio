import os

from apps.authentication.models import Portfolio, ContactUs
from apps.home import blueprint
from flask import render_template, redirect, url_for, request, send_from_directory, current_app
from flask_login import current_user, login_required
from apps.authentication.forms import ContactUsForm, AddPortfolioForm
from functools import wraps
from flask import abort
from apps import db
from datetime import datetime

from main import app


# Admin only decorator
def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return func(*args, **kwargs)

    return decorated_function


@blueprint.route('/')
def index():
    contact_us_form = ContactUsForm()
    all_portfolio = db.session.query(Portfolio).all()
    return render_template('home/index.html', all_portfolio=all_portfolio, form=contact_us_form,
                           logged_in=current_user.is_authenticated, current_user=current_user)


@blueprint.route("/portfolio/<int:portfolio_id>", methods=["GET", "POST"])
def portfolio(portfolio_id):
    comment_form = AddPortfolioForm()
    portfolio_to_view = db.session.query(Portfolio).filter_by(id=int(portfolio_id)).first()

    if request.method == "POST" and comment_form.validate_on_submit():
        # write comment to db
        # new_comment = Comment(comment=request.form["comment"],
        #                       comment_author=current_user,
        #                       author_post=post_to_read
        #                       )
        # db.session.add(new_comment)
        # db.session.commit()
        return redirect(url_for("home_blueprint.portfolio", portfolio_id=portfolio_id))

    return render_template("home/portfolio_details.html", logged_in=current_user.is_authenticated,
                           portfolio=portfolio_to_view, form=comment_form)


@blueprint.route("/add", methods=["GET", "POST"])
@login_required
@admin_only
def add():
    add_portfolio_form = AddPortfolioForm()
    if request.method == "POST" and add_portfolio_form.validate_on_submit():
        new_portfolio = Portfolio(
            title=request.form["title"],
            category=request.form["category"],
            date=request.form["date"],
            img_url=request.form["img_url"],
            github_url=request.form["github_url"],
            final_project=request.form["final_project"],
            download=request.form["download"],
            client=request.form["client"],
            body=request.form["body"],
        )
        db.session.add(new_portfolio)
        db.session.commit()
        return redirect(url_for("home_blueprint.index"))

    return render_template("home/add.html", form=add_portfolio_form)


@blueprint.route("/edit", methods=["GET", "POST"])
@login_required
@admin_only
def edit():
    edit_portfolio_form = AddPortfolioForm()
    if request.method == "POST":
        portfolio_id = request.args.get('portfolio_id')
        portfolio_to_update = db.session.query(Portfolio).get(int(portfolio_id))
        portfolio_to_update.title = request.form["title"]
        portfolio_to_update.category = request.form["category"]
        portfolio_to_update.img_url = request.form["img_url"]
        portfolio_to_update.date = request.form["date"]
        portfolio_to_update.github_url = request.form["github_url"]
        portfolio_to_update.client = request.form["client"]
        portfolio_to_update.final_project = request.form["final_project"]
        portfolio_to_update.download = request.form["download"]
        portfolio_to_update.body = request.form["body"]
        db.session.commit()
        return redirect(url_for('home_blueprint.index'))
    portfolio_id = request.args.get('portfolio_id')
    portfolio_selected = db.session.query(Portfolio).filter_by(id=int(portfolio_id)).first()
    return render_template("home/edit.html", portfolio=portfolio_selected, form=edit_portfolio_form)


@blueprint.route("/delete", methods=["GET", "POST"])
@login_required
@admin_only
def delete():
    portfolio_id = request.args.get('portfolio_id')
    portfolio_to_delete = Portfolio.query.get(int(portfolio_id))
    db.session.delete(portfolio_to_delete)
    db.session.commit()
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/download')
def download():
    return send_from_directory(directory='static', path="file/PY.DEVELOPER CV PDF.pdf")


@blueprint.route("/contact-me", methods=['GET', 'POST'])
def contact_us():
    contact_us_form = ContactUsForm()
    if request.method == "POST" and contact_us_form.validate_on_submit():
        name = contact_us_form.name.data
        email = contact_us_form.email.data
        message = contact_us_form.message.data
        message_to_us = ContactUs(
            name=name,
            email=email,
            message=message,
            date=datetime.now().date()
        )
        db.session.add(message_to_us)
        db.session.commit()

        return render_template("home/successful.html")
    return render_template("home/contact_us.html", form=contact_us_form)
