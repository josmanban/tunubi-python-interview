import os
import tempfile
import pytest
import pdb
import json
from util.mongo_client_wrapper import MongoAPI

from app import *


@pytest.fixture(scope="class")
def client():
    pdb.set_trace()
    with app.test_client() as client:
        with app.app_context():
            app.config['TESTING']=True
            app.config['DB_NAME']='test_polls'
        yield client

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
