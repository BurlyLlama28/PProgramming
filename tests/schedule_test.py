import pytest
import json

mimetype = 'application/json'
headers = {
    'Content-Type': mimetype,
    'Accept': mimetype
}
user = {
    'full_name': 'Vitalii Yarmus',
    'birthday': '2002-10-10',
    'email': 'test@test.com',
    'phone_number': '0983057271',
    'password': '12345'
}

login_data = {
    'email': 'test@test.com',
    'password': '12345'
}

film_data = {
    'name': 'test_name',
    'duration': 100
}

schedule_data = {
    'date': '2020-10-10',
    'films': [
        {
            'film_id': 1,
            'start_time': '13:11:00',
            'end_time': '14:15:00'
        }
    ]
}

schdeule_update_data = {
    'date': '2020-10-11',
    'films': [
        {
            'film_id': 1,
            'start_time': '13:11:00',
            'end_time': '14:15:00'
        }
    ]
}

def create_user(client):
    resp = client.post('/user', data=json.dumps(user), headers=headers)
    assert resp.content_type == mimetype
    assert resp.status_code == 201

    resp = client.post('/user', data=json.dumps({}), headers=headers)
    assert resp.status_code == 400

def login(client, login):
    resp = client.get('/user/login', data=json.dumps(login), headers=headers)
    assert resp.content_type == mimetype
    assert resp.status_code == 200
    json_token = resp.data.decode('utf8').replace("'", '"')
    return json.loads(json_token).get('access_token')

def create_film(client):
    create_user(client)
    token = login(client, login_data)
    resp = client.post('/film', data=json.dumps(film_data), headers={
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer ' + token
    })
    assert resp.content_type == mimetype
    assert resp.status_code == 201
    return token

def create_schedule(client):
    token = create_film(client)

    resp = client.post('/schedule', data=json.dumps(schedule_data), headers={
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer ' + token
    })

    assert resp.status_code == 201

    return token

def test_schedule_post(client):
    token = create_schedule(client)

    resp = client.post('/schedule', data=json.dumps(schedule_data), headers={
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer ' + token
    })

    assert resp.status_code == 409

def test_schedule_get(client):
    respNotFound = client.get('/schedule')
    assert respNotFound.status_code == 404

    create_schedule(client)

    respOk = client.get('/schedule')
    assert respOk.status_code == 200
    
def test_schedule_get_by_id(client):
    respNotFound = client.get('/schedule/1')
    assert respNotFound.status_code == 404

    respNotFound = client.get('/schedule/gsdb')
    assert respNotFound.status_code == 400

    create_schedule(client)

    respOk = client.get('/schedule')
    assert respOk.status_code == 200

def test_schedule_update(client):
    token = create_schedule(client)

    resp = client.put('/schedule/1', data=json.dumps(schedule_data), headers={
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer ' + token
    })

    assert resp.status_code == 202