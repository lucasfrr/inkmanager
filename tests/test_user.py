from http import HTTPStatus
from uuid import uuid4

from .factories import UserFactory


def test_create_user(client):
    response = client.post(
        url='/users/register',
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


def test_try_create_user_with_an_existing_email(client, session):
    user = UserFactory.create(email='yamandu@gmail.com')

    session.add(user)
    session.commit()

    response = client.post(
        url='/users/register',
        json={
            'username': 'yamanducosta',
            'email': 'yamandu@gmail.com',
            'fullname': 'Yamandu Costa',
            'password': 'nossasenha'
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'email already exists'}


def test_try_create_user_with_an_existing_username(client, session):
    user = UserFactory.create(username='kikoloureiro')

    session.add(user)
    session.commit()

    response = client.post(
        url='/users/register',
        json={
            'username': 'kikoloureiro',
            'email': 'kikoloureiro@gmail.com',
            'fullname': 'Kiko Loureiro',
            'password': 'tuasenha'
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'username already exists'}


def test_update_user(client, user, token):
    response = client.put(
        url=f'/users/update/{user.id}',
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


def test_update_user_with_wrong_user(client, token):
    wrong_id = str(uuid4())
    response = client.put(
        url=f'/users/update/{wrong_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'toniboy',
            'email': 'toniboy@test.com',
            'password': 'senha nova',
            'fullname': 'Toni Boy',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        url=f'/users/delete/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'detail': 'user has been deleted'}


def test_delete_user_with_wrong_user(client, other_user, token):
    response = client.delete(
        url=f'/users/delete/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'not enough permissions'}
