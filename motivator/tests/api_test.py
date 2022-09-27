import pytest
from unittest.mock import patch
from users.views import get_motivations
import requests
import requests_mock

def test_response(url):
    with requests_mock.Mocker() as m:
        m.get(url, status_code = 200)
        response = requests.get(url)
        assert response.status_code == 200

def test_invalid_response(url):
    response = requests.get(url)
    assert response.status_code == 403


def test_post(url):
    with requests_mock.Mocker() as m:
        data = {
            'nickname': 'Test',
            'motivation': 'Test motivation',
            'is_visible': True
        }
        m.post(url, json = data, status_code = 201)
        response = requests.post(url, data=data)
        print(response.json())
        assert response.status_code == 201
        assert response.json() == data

def test_get_random(url):
    with requests_mock.Mocker() as m:
        random_url = url + 'random/'
        m.get(random_url)
        response = requests.get(random_url)
        assert response.status_code == 200
