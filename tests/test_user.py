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


def test_update_user(client, user, token):
    response = client.put(
        f'/users/update/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'toniboy',
            'email': 'toniboy@test.com',
            'password': 'senha nova',
            'fullname': 'Toni Boy',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == 'toniboy'
    assert response.json()['email'] == 'toniboy@test.com'


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/delete/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'detail': 'user has been deleted'}
