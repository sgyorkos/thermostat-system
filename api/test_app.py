import json
import os
import pytest
import tempfile

from api import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mocked_data_fs(fs):
    contents = {
        "lights": [
            {
                "name": "light1",
                "on": 1
            },
            {
                "name": "light2",
                "on": 0
            },
            {
                "name": "light3",
                "on": 1
            }
        ],
        "thermostat": {
            "temperature": 72,
            "unit": "F"
        }
    }
    fs.create_file('data.json', contents=json.dumps(contents))
    yield fs
