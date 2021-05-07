import json
import pytest

from test_app import client, mocked_data_fs


def test_get_all_lights(client, mocked_data_fs):
    response = client.get('/light', data={}, follow_redirects=True)
    assert '200' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == "Found all lights"
    assert len(data['lights']) == 3
    assert data['lights'][0] == {"name": "light1", "on": 1}
    assert data['lights'][1] == {"name": "light2", "on": 0}
    assert data['lights'][2] == {"name": "light3", "on": 1}

def test_get_all_lights_no_lights(client, fs):
    contents = {
        "lights": [],
        "thermostat": {
            "temperature": 72,
            "unit": "F"
        }
    }
    fs.create_file('data.json', contents=json.dumps(contents))
    response = client.get('/light', follow_redirects=True)
    assert '200' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == "Found all lights"
    assert len(data['lights']) == 0

def test_get_all_lights_no_lights_entry(client, fs):
    contents = {
        "thermostat": {
            "temperature": 72,
            "unit": "F"
        }
    }
    fs.create_file('data.json', contents=json.dumps(contents))
    response = client.get('/light', follow_redirects=True)
    assert '200' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == "Found all lights"
    assert len(data['lights']) == 0

def test_get_light(client, mocked_data_fs):
    response = client.get('/light', query_string={"name": "light2"}, follow_redirects=True)
    assert '200' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == "Found light [light2]"
    assert data['light'] == {"name": "light2", "on": 0}

def test_get_light_non_existent(client, mocked_data_fs):
    response = client.get('/light', query_string={"name": "light4"}, follow_redirects=True)
    assert '404' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert "Light [light4] not found" in data['error']

def test_add_light(client, mocked_data_fs):
    response = client.post('/light', query_string={"name": "light4", "new":""}, follow_redirects=True)
    assert '200' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == "Light [light4] added"
    with open('data.json') as data_file:
        contents = json.load(data_file)
        assert contents['lights'][3] == {"name": "light4", "on": 0}

def test_add_light_already_exists(client, mocked_data_fs):
    response = client.post('/light', query_string={"name": "light2", "new":""}, follow_redirects=True)
    assert '400' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert "Light [light2] already exists" in data['error']

def test_add_light_no_name(client, mocked_data_fs):
    response = client.post('/light', query_string={"new":""}, follow_redirects=True)
    assert '400' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert "No name given" in data['error']

def test_flip_light(client, mocked_data_fs):
    response = client.post('/light', query_string={"name": "light2"}, follow_redirects=True)
    assert '200' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == "Light [light2] flipped"
    with open('data.json') as data_file:
        contents = json.load(data_file)
        assert contents['lights'][1] == {"name": "light2", "on": 1}

def test_flip_light_non_existent(client, mocked_data_fs):
    response = client.post('/light', query_string={"name": "light4"}, follow_redirects=True)
    assert '404' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert "Light [light4] not found" in data['error']

def test_flip_light_no_name(client, mocked_data_fs):
    response = client.post('/light', query_string={}, follow_redirects=True)
    assert '400' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert "No name given" in data['error']

def test_delete_light(client, mocked_data_fs):
    response = client.delete('/light', query_string={"name": "light2"}, follow_redirects=True)
    assert '200' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == "Light [light2] deleted"
    with open('data.json') as data_file:
        contents = json.load(data_file)
        assert len(contents['lights']) == 2
        assert contents['lights'][0] == {"name": "light1", "on": 1}
        assert contents['lights'][1] == {"name": "light3", "on": 1}

def test_delete_light_non_existent(client, mocked_data_fs):
    response = client.delete('/light', query_string={"name": "light4"}, follow_redirects=True)
    assert '200' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == "Light [light4] deleted"
    with open('data.json') as data_file:
        contents = json.load(data_file)
        assert len(contents['lights']) == 3
        assert contents['lights'][0] == {"name": "light1", "on": 1}
        assert contents['lights'][1] == {"name": "light2", "on": 0}
        assert contents['lights'][2] == {"name": "light3", "on": 1}

def test_delete_light_no_name(client, mocked_data_fs):
    response = client.delete('/light', follow_redirects=True)
    assert '400' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert "No name given" in data['error']

def test_get_thermostat(client, mocked_data_fs):
    response = client.get('/thermostat', follow_redirects=True)
    assert '200' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == 'Found thermostat'
    assert data['thermostat'] == {"temperature": 72, "unit": "F"}

def test_get_thermostat_no_data(client, fs):
    fs.create_file('data.json', contents="{ }")
    response = client.get('/thermostat', follow_redirects=True)
    assert '404' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert 'Thermostat not found' in data['error']

def test_update_thermostat_change_unit(client, mocked_data_fs):
    response = client.post('/thermostat', query_string={'unit': 'C'}, follow_redirects=True)
    assert '200' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == "Thermostat updated"
    with open('data.json') as data_file:
        contents = json.load(data_file)
        assert contents['thermostat'] == {'temperature': 22, 'unit': 'C'}

def test_update_thermostat_change_temperature(client, mocked_data_fs):
    response = client.post('/thermostat', query_string={'temperature': 68}, follow_redirects=True)
    assert '200' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == "Thermostat updated"
    with open('data.json') as data_file:
        contents = json.load(data_file)
        assert contents['thermostat'] == {'temperature': 68, 'unit': 'F'}

def test_update_thermostat_change_temperature_and_unit(client, mocked_data_fs):
    response = client.post('/thermostat', query_string={'temperature': 20, 'unit': 'C'}, follow_redirects=True)
    assert '200' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert data['message'] == "Thermostat updated"
    with open('data.json') as data_file:
        contents = json.load(data_file)
        assert contents['thermostat'] == {'temperature': 20, 'unit': 'C'}

def test_update_thermostat_invalid_unit(client, mocked_data_fs):
    response = client.post('/thermostat', query_string={'unit': 'A'}, follow_redirects=True)
    assert '400' in response.status
    data = json.loads(response.data.decode('utf-8'))
    assert "Unit must be either 'C' or 'F'" in data['error']