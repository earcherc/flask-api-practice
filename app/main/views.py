from flask import current_app, redirect, render_template, session, url_for

from .. import db
from ..models import User
from . import main
from .forms import NameForm


def index():
    form = NameForm()
    # If form has a name value, as it is required
    if form.validate_on_submit():
        # If User table has a username that matches the form data
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            # If not then create the user and add known to the flask session
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session["known"] = False
        else:
            session["known"] = True
        session["name"] = form.name.data
        # Reset th form data after submitting
        form.name.data = ""
        # Post/redirect/get pattern on refresh
        return redirect(url_for("main.index"))
    # If we access index with just a get request we render template with session vars
    return render_template(
        "index.html",
        form=form,
        name=session.get("name"),
        known=session.get("known", False),
    )


main.add_url_rule("/", view_func=index, methods=["GET", "POST"])
