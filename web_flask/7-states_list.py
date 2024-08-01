#!/usr/bin/python3
"""
Starts a Flask web application
"""
from flask import Flask, render_template
from models.state import State
from models import storage


app = Flask(__name__)

@app.teardown_appcontext
def close_storage(exception):
    """Closes the storage on teardown"""
    storage.close()

@app.route('/states_list', strict_slashes=False)
def states():
    """Lists states"""
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run()
