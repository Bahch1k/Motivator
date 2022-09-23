import pytest


@pytest.mark.django_db
def test_register(user, client):
    url = '/users/register/'
    # payload = user
    response = client.post(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_login(client):
    url = '/users/login/'
    # payload = user

    # client.post('/users/register/', payload)
    response = client.post(url, dict(username='Tst_user', password='Testpassword'))

    assert response.status_code == 200