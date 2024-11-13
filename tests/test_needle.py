from http import HTTPStatus

from .factories import NeedleFactory


def test_create_needle(client, user, token):
    user_id = str(user.id)

    response = client.post(
        url='/needles/create',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Cartucho universal pro',
            'brand': 'Electric Ink',
            'model': 'RS',
            'size': '1009',
            'amount': 20,
            'user_id': user_id,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['model'] == 'RS'
    assert response.json()['size'] == '1009'


def test_get_needle(client, session, token, user):
    needle = NeedleFactory.create(user_id=user.id)

    session.add(needle)
    session.commit()

    needle_id = str(needle.id)

    response = client.get(
        url=f'/needles/{needle.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == needle_id


def test_inexistent_needle(client, token):
    response = client.get(
        url='/needles/588e7991-ccb1-481b-aa11-048a387744ab',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'needle not found'}


def test_list_all_needles(client, user, token, session):
    expected = 15
    session.bulk_save_objects(NeedleFactory.create_batch(15, user_id=user.id))
    session.commit()

    response = client.get(
        url='/needles', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['needles']) == expected


def test_list_with_default_filter_value(client, user, token, session):
    expected = 20
    session.bulk_save_objects(NeedleFactory.create_batch(30, user_id=user.id))
    session.commit()

    response = client.get(
        url='/needles', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['needles']) == expected


def test_change_needle(client, session, user, token):
    needle = NeedleFactory.create(user_id=user.id)

    session.add(needle)
    session.commit()

    response = client.patch(
        url=f'/needles/update/{needle.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'WJX Pro', 'brand': 'WJX', 'model': 'RL'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'WJX Pro'
    assert response.json()['brand'] == 'WJX'
    assert response.json()['model'] == 'RL'


def test_try_update_wrong_needle(client, token):
    response = client.patch(
        url='/needles/update/508e7991-ccb1-481b-aa11-048a387744ab',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'WJX Pro', 'brand': 'WJX', 'model': 'RL'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'needle not found'}


def test_delete_needle(client, token, user, session):
    needle = NeedleFactory.create(user_id=user.id)

    session.add(needle)
    session.commit()

    response = client.delete(
        url=f'/needles/delete/{needle.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'detail': 'needle has been deleted'}


def test_delete_inexistent_needle(client, token):
    response = client.delete(
        url='/needles/delete/508e7991-ccb1-481b-aa11-048a387744ab',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'needle not found'}
