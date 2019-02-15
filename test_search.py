import os
import pytest
from app import app
from flask import json


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_index(client):
    rv = client.get('/')
    assert rv.data is not None

def test_get_stores(client):
    rv = client.get('/get-stores?searchString=hav')
    resultList = json.loads(rv.data)
    assert {"name": "Newhaven", "postcode": "BN9 0AG"} in resultList
    assert len(resultList) == 2

