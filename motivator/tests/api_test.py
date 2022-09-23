import pytest
from unittest.mock import patch
from users.views import get_motivations
import requests_mock

@requests_mock.Mocker()
def test_response(url, mocker):

    mocker.get(url).status_code = 200

    response = get_motivations(url)

    assert response == 200

# def test_invalid_response(url):
#     response = requests.get(url)
#     assert response.status_code == 403
