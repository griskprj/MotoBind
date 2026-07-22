import json
from datetime import datetime


def test_register_success(client):
    """ Тест успешной регистрации """
    response = client.post('/api/auth/register', json={
        'email': 'newuser@example.com',
        'password': 'password123',
        'username': 'newuser',
        'role': 'motorcyclist'
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Регистрация успешна'
    assert data['user']['email'] == 'newuser@example.com'
    assert data['user']['username'] == 'newuser'
