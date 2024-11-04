from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/users/register',
        json={
            'username': 'joao',
            'email': 'joao@gmail.com',
            'fullname': 'Joao Felix',
            'password': 'minhasenha',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['email'] == 'joao@gmail.com'
    assert response.json()['username'] == 'joao'
