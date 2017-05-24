# backend server of ZoomProof
## requirements
* python >= `3.4`
* install required python packages via `pip install -r requirements.txt` from `requirements.txt`
* `djvutoxml` command line tool (e.g. installed on a Ubuntu system via `sudo apt-get install djvulibre-bin`)

## running tests
`python -m unittest discover ./tests/`

## running the server
the server needs 3 components to run
 1. `redis` database server, start via `redis-server` (note: you do not need to start your own server when deploying on Wikitech Tool Lab, also make sure to use the 'production' settings in `app.py` when doing so)
 2. `celery` task queue, start via `celery worker -A app.celery` (n.b. that the `{}.celery` part has to be the same as the name of the python module where the `celery` object will be created (which is in `app.py` in our case))
 3. `flask` web framework, start via `export FLASK_APP=app.py` and then `flask run` (note: does not need to be started like this in a production environment, there a wsgi or uwsgi compatible web server will start the flask app)

## component explanation
* `redis` is used for handling `celery`s task queue and also for a thread-safe lookup of which `.djvu` files we are currently converting, such that we never start a conversion twice on subsequent requests
* `celery` is used for spawning asynchronous tasks such that the conversion of a `.djvu` file (which can take a couple of minutes) is done in a non-blocking fashion
* `flask` is a minimal web framework for python and is used to implement the backend API

## API endpoints
`/sha1/page_int`
 * will return `{page_int}.json` for the `.djvu` file specified by the `sha1` if already cached
 * will start conversion of the `.djvu` file specified by the `sha1` if not already cached and return a JSON notification about that
