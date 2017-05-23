# backend server of ZoomProof
## requirements
* python >= `3.5`
* install required python packages via `pip install -r requirements.txt` from `requirements.txt`

## running the server
* the server needs 3 components to run
 1. `redis` database server, start via `redis-server`
 2. `celery` task queue, start via `celery worker -A server.celery` (n.b. that the `{}.celery` part has to be the same as the name of the python module where the `celery` object will be created (which is in `server.py` in our case))
 3. `flask` web framework, start via `export FLASK_APP=server.py` and then `flask run`

## component explanation
* `redis` is used for handling `celery`s task queue and also for a thread-safe lookup of which `.djvu` files we are currently converting, such that we never start a conversion twice on subsequent requests
* `celery` is used for spawning asynchronous tasks such that the conversion of a `.djvu` file (which can take a couple of minutes) is done in a non-blocking fashion
* `flask` is a minimal web framework for python and is used to implement the backend API

## API endpoints
* `/sha1/page\_int`
 * will return `page\_int.json` for the `.djvu` file specified by the `sha1` if already cached
 * will start conversion of the `.djvu` file specified by the `sha1` if not already cached and return a JSON notification about that
