import pytest

def test_app(client):
    resp = client.get('/')
    assert resp.status_code == 200