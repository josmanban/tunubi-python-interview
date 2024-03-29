from flask import Flask, request, json, Response
from flask import Flask, request, json, Response
from util.mongo_client_wrapper import MongoAPI
from werkzeug.exceptions import HTTPException, BadRequest

import pdb


app = Flask(__name__)
app.config['DB_NAME'] = 'polls'


@app.route('/')
def base():
    return "status:up"


@app.route('/add-answer', methods=('POST',))
def answers_post():
    data = request.json
    res = MongoAPI(app.config['DB_NAME'], "answers").write(data)
    return Response(
        response=json.dumps(res),
        status=200,
        mimetype='application/json')


@app.route('/add-poll', methods=('POST',))
def polls_post():
    data = request.json
    res = MongoAPI(app.config['DB_NAME'], "polls").write(data)
    return Response(
        response=json.dumps(res),
        status=200,
        mimetype='application/json')


@app.route('/get-polls')
def polls_get():
    db_name = app.config['DB_NAME']
    polls = MongoAPI(db_name, "polls").read_polls()
    return Response(
        response=json.dumps(polls),
        status=200,
        mimetype='application/json')


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    print('up')
    app.run(host='0.0.0.0', debug=True)
