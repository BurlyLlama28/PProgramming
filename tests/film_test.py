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

film_data_update = {
    'name': 'test_name 2',
    'duration': 100
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

def test_film_post(client):
    token = create_film(client)

    resp = client.post('/film', headers={
        'Authorization': 'Bearer ' + token
    })
    assert resp.status_code == 400

    respNotValidBody = client.post('/film', data=json.dumps({}), headers={
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer ' + token
    })
    assert respNotValidBody.content_type == mimetype
    assert respNotValidBody.status_code == 400

    respConflict = client.post('/film', data=json.dumps(film_data), headers={
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer ' + token
    })
    assert respConflict.content_type == mimetype
    assert respConflict.status_code == 409

def test_get_film(client):
    respNotFound = client.get('/film/1')
    assert respNotFound.status_code == 404

    respBad = client.get('/film/gie')
    assert respBad.status_code == 400

    create_film(client)

    respFound = client.get('/film/1')
    assert respFound.status_code == 200

def test_get_films(client):
    respNotFound = client.get('/film')
    assert respNotFound.status_code == 404

    create_film(client)

    respFound = client.get('/film')
    assert respFound.status_code == 200

def test_update_film(client):
    token = create_film(client)
    resp = client.put('/film/1', data=json.dumps(film_data_update), headers={
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer '+ token
    })
    assert resp.status_code == 202

    respWrong = client.put('/film/1', data=json.dumps(film_data_update), headers={
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDkwMDE0MDEsIm5iZiI6MTYwOTAwMTQwMSwianRpIjoiZGFiNGZiZjMtNzU0NC00YWE0LTk3ODctMDMzODQ2OGU1NmI3IiwiZXhwIjoxNjA5MDAyMzAxLCJpZGVudGl0eSI6InRlc3QxQHRlc3QuY29tIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.5LUYCBtY7J5sbxDc0dueslHNQ5hXY0G_yi2ATW44ojw'
    })
    assert respWrong.status_code == 401

    respNotFound = client.put('/film/5', data=json.dumps(film_data_update), headers={
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer '+ token
    })
    assert respNotFound.status_code == 404

    respWrongId = client.put('/film/1', data=json.dumps({}), headers={
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer '+ token
    })
    assert respWrongId.status_code == 400

def test_delete(client):
    token = create_film(client)
    resp = client.delete('/film/1', headers={
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer '+ token
    })
    assert resp.status_code == 200

    resp = client.delete('/film/1', headers={
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer '+ token
    })
    assert resp.status_code == 404