#!/usr/bin/python3
"""
Starts a Flask web application
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Returns a Hello"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Returns HBNB"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """Return C text value"""
    text = text.replace('_', ' ')
    return f"C {text}"


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def pyth(text="is cool"):
    """Return Python text"""
    text = text.replace('_', ' ')
    return f"Python {text}"


@app.route("/number/<int:n>", strict_slashes=False)
def is_num(n):
    """Accepts only numbers"""
    return f"{n} is a number"


if __name__ == "__main__":
    app.run()
