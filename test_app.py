import os
import tempfile
import pytest
import pdb
import json
from util.mongo_client_wrapper import MongoAPI
import datetime
from app import *


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            app.config['TESTING'] = True
            app.config['DB_NAME'] = 'test_polls'
            db = MongoAPI("test_polls", "polls")
            db.write_bulk([
                {
                    "question": "foo?",
                    "CreatedDate": datetime.datetime.today()
                },
                {
                    "question": "foo?",
                    "CreatedDate": datetime.datetime.today()
                },
                {
                    "question": "foo?",
                    "CreatedDate": datetime.datetime.today()
                },
            ])
        yield client
        db.delete_many({})


def test_list_polls(client):
    rv = client.get('/get-polls')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data is not None
    assert len(json_data) > 0


def test_polls_post(client):
    rv = client.post(
        '/add-poll',
        json={"poll": "foo"},
        follow_redirects=True
    )
    new_id = rv.get_json()
    assert rv.status_code == 200
    assert new_id is not None

    db = MongoAPI(app.config['DB_NAME'], "polls")
    polls = db.read()
    assert polls[-1]['_id'] == new_id


def test_answers_post(client):
    db = MongoAPI(app.config['DB_NAME'], "polls")
    polls = db.read()
    last_poll = polls[-1]

    rv = client.post(
        '/add-answer',
        json={
            "poll_id": last_poll['_id'],
            "answer": "foo"
        }
    )
    new_id = rv.get_json()
    assert rv.status_code == 200
    assert new_id is not None

    db_answers = MongoAPI(app.config['DB_NAME'], "answers")
    answers = db_answers.read()
    last_answer = answers[-1]
    assert new_id == last_answer["_id"]


def test_not_found(client):
    rv = client.get("/get-foo")
    assert rv.status_code == 404
    assert rv.get_json()["name"] == "Not Found"


def test_not_allowed_method(client):
    rv = client.get("/add-poll")
    assert rv.status_code == 405
    assert rv.get_json()["name"] == "Method Not Allowed"
