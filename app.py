from flask import Flask

app = Flask(__name__)


def index():
    return "<h1>Hello World!</h1>"


def user(name):
    return "<h1>Hello, {}!</h1>".format(name)


app.add_url_rule("/", "index", index)

app.add_url_rule("/user/<name>", "user", user)
