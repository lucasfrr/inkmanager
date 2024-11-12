from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        url='/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_token_expired_after_time(client, user):
    with freeze_time('2024-11-09 12:00:00'):
        response = client.post(
            url='/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2024-11-09 12:31:00'):
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

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'could not validate credentials'}


def test_token_inexistent_user(client):
    response = client.post(
        url='/auth/token',
        data={'username': 'no_user@no_domain.com', 'password': 'testtest'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'incorrect email or password'}


def test_token_wrong_password(client, user):
    response = client.post(
        url='/auth/token',
        data={'username': user.email, 'password': 'essanaoeasenhad'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'incorrect email or password'}


def test_refresh_token(client, token):
    response = client.post(
        url='/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2024-11-09 12:00:00'):
        response = client.post(
            url='/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )

    assert response.status_code == HTTPStatus.OK
    token = response.json()['access_token']

    with freeze_time('2024-11-09 12:31:00'):
        response = client.post(
            url='/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'could not validate credentials'}
