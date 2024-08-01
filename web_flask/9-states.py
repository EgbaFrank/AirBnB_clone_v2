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


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """Lists cities by states"""
    states = storage.all(State)
    if not id:
        return render_template('9-states.html', states=states)
    else:
        key = f"State.{id}"
        state = states.get(key)

        return render_template('9-states.html', state=state)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
