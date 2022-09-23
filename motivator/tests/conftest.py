import pytest
from dotenv import load_dotenv
import os
from django.test import Client as test_client

load_dotenv()

@pytest.fixture
def client():
    client = test_client()
    return client

@pytest.fixture
def user():
    user = {
        'username': 'Test_user',
        'password': 'Testpassword',
    }
    return user


@pytest.fixture
def header():
    header = {
        'Authorization': os.getenv('API_KEY')
    }
    return header

@pytest.fixture
def url():
    url = os.getenv('API_URL')
    return url

