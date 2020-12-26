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

user_update = {
    'full_name': 'Vitalii Yarmus 2',
    'birthday': '2002-10-10',
    'email': 'test@test.com',
    'phone_number': '0983057271',
    'password': '12345'
}

login_data = {
    'email': 'test@test.com',
    'password': '12345'
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

def test_post_user(client):
    resp = client.post('/user', data=json.dumps({}), headers=headers)
    assert resp.status_code == 400

    resp = client.post('/user')
    assert resp.status_code == 400

    create_user(client)

    resp = client.post('/user', data=json.dumps(user), headers=headers)
    assert resp.content_type == mimetype
    assert resp.status_code == 409

def test_login(client):
    create_user(client)
    login(client, login_data)

def test_get(client):
    create_user(client)
    token = login(client, login_data)
    resp = client.get('/user/1', headers={
        'Authorization': 'Bearer '+ token
    })
    assert resp.content_type == mimetype
    assert resp.status_code == 200

    respWrong = client.get('/user/1', headers={
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDkwMDE0MDEsIm5iZiI6MTYwOTAwMTQwMSwianRpIjoiZGFiNGZiZjMtNzU0NC00YWE0LTk3ODctMDMzODQ2OGU1NmI3IiwiZXhwIjoxNjA5MDAyMzAxLCJpZGVudGl0eSI6InRlc3QxQHRlc3QuY29tIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.5LUYCBtY7J5sbxDc0dueslHNQ5hXY0G_yi2ATW44ojw'
    })
    assert respWrong.status_code == 401

    respNotFound = client.get('/user/5', headers={
        'Authorization': 'Bearer '+ token
    })
    assert respNotFound.status_code == 404

    respWrongId = client.get('/user/gsbgd', headers={
        'Authorization': 'Bearer '+ token
    })
    assert respWrongId.status_code == 400

def test_update(client):
    respUnauth = client.put('/user/1', data=json.dumps({}), headers=headers)
    assert respUnauth.status_code == 401

    create_user(client)
    token = login(client, login_data)

    haders_auth = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer '+ token
    }

    respNotFound = client.put('./user/5', headers=haders_auth)
    assert respNotFound.status_code == 404

    resp = client.put('/user/1', data=json.dumps(user_update), headers=haders_auth)
    assert resp.status_code == 202