#!/usr/bin/python3
"""
Starts a Flask web application
"""
from flask import Flask, render_template

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

@app.route("/number_template/<int:n>", strict_slashes=False)
def num_temp(n):
    """Renders a HTML template"""
    return render_template("5-number.html", num=n)


if __name__ == "__main__":
    app.run()
