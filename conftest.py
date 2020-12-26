import pytest
from config import *
from app import create_app

@pytest.fixture
def app():
    testApp = create_app()
    return testApp