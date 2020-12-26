import pytest
import json
from datetime import date

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        'full_name': 'Vitalii Yarmus',
        'birthday': '2002-10-10',
        'email': 'test@test.com',
        'phone_number': '0983057271',
        'password': '12345'
    }

def test_post_user(client):
    resp = client.post('/user', data=json.dumps(data), headers=headers)
    assert resp.content_type == mimetype
    assert resp.status_code == 201

def test_login(client):
    resp = client.get('/user/login', data=json.dumps(data), headers=headers)
    assert resp.content_type == mimetype
    assert resp.status_code == 200