from flask import Flask, flash, redirect, render_template, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "blahblahblah"


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("You have changed your name")
        session["name"] = form.name.data
        return redirect(url_for("index"))
    return render_template("index.html", form=form, name=session.get("name"))


def page_not_found(e):
    return "<h1>Page not found!</h1>", 404


def internal_server_error(e):
    return "<h1>Bad request!</h1>", 500


app.add_url_rule("/", view_func=index, methods=["GET", "POST"])

app.register_error_handler(404, page_not_found)

app.register_error_handler(500, internal_server_error)
