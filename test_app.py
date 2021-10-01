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
            app.config['TESTING']=True
            app.config['DB_NAME']='test_polls'
            db = MongoAPI("test_polls","polls")
            db.write_bulk([
                {
                    "poll":"foo?",
                    "CreatedDate": datetime.datetime.today()
                },
                {
                    "poll":"foo?",
                    "CreatedDate": datetime.datetime.today()
                },
                {
                    "poll":"foo?",
                    "CreatedDate": datetime.datetime.today()
                },
            ])
        yield client
        db.delete_many({})

def test_list_polls(client):
    rv = client.get('/getPolls')
    json_data = rv.get_json()
    assert json_data is not None
    assert len(json_data) > 0

def test_polls_post(client):
    rv = client.post(
        '/addPoll',
        json={"poll":"foo"},
        follow_redirects=True
    )
    new_id = rv.get_json()
    assert new_id is not None

    rv = client.get('/getPolls')
    json_data = rv.get_json()
    assert len(json_data) > 0
    assert json_data[-1]['_id'] == new_id
