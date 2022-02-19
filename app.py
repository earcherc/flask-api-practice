import os

from flask import Flask, redirect, render_template, session, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Role(db.Model):
    # Explicitly set the table name to follow good convention of plural table names
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    # Contains the back reference to the relationship so we can access role.users.all()
    # lazy loaded so we can add filters if we query the relationship form this direction.
    users = db.relationship("User", backref="role", lazy="dynamic")

    # Not necessary but good for debugging
    def __repr__(self):
        return "<Role %s>" % self.name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    age = db.Column(db.Integer)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<User %s>" % self.username


# Flask-WTF forms
class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


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
        return redirect(url_for("index"))
    # If we access index with just a get request we render template with session vars
    return render_template(
        "index.html",
        form=form,
        name=session.get("name"),
        known=session.get("known", False),
    )


def page_not_found(e):
    return "<h1>Page not found!</h1>", 404


def internal_server_error(e):
    return "<h1>Bad request!</h1>", 500


app.add_url_rule("/", view_func=index, methods=["GET", "POST"])

app.register_error_handler(404, page_not_found)

app.register_error_handler(500, internal_server_error)

# To set the imports for flask shell automatically on init
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
