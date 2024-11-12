from http import HTTPStatus

from .factories import InkFactory


def test_create_ink(client, token, user):
    user_id = str(user.id)

    response = client.post(
        url='/inks/create',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Tinta Easy Glow',
            'brand': 'Electric Ink',
            'color': 'Blue',
            'in_use': True,
            'weight': '15g',
            'user_id': user_id,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Tinta Easy Glow'
    assert response.json()['weight'] == '15g'


def test_list_all_inks(client, session, user, token):
    expected = 10
    session.bulk_save_objects(InkFactory.create_batch(10, user_id=user.id))
    session.commit()

    response = client.get(
        url='/inks', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['inks']) == expected


def test_list_inks_should_return_5(client, user, token, session):
    expected = 5

    session.bulk_save_objects(
        InkFactory.create_batch(
            6, user_id=user.id
        )
    )
    session.commit()

    response = client.get(
        url='/inks/?offset=1&limit=5',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['inks']) == expected


def test_link_inks_by_brand_should_return_3(client, user, token, session):
    expected = 3

    session.bulk_save_objects(
        InkFactory.create_batch(3, brand='Electric Ink', user_id=user.id)
    )
    session.commit()

    response = client.get(
        url='/inks/?brand=electric ink',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['inks']) == expected


def test_change_ink(client, session, user, token):
    ink = InkFactory.create(
        brand='Electric Ink',
        color='Reddish',
        user_id=user.id
    )

    session.add(ink)
    session.commit()

    response = client.patch(
        url=f'/inks/update/{ink.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'brand': 'Solid Ink',
            'color': 'Magenta',
            'weight': '30ml'
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['brand'] == 'Solid Ink'
    assert response.json()['color'] == 'Magenta'
    assert response.json()['weight'] == '30ml'


def test_change_wrong_ink(client, token):
    response = client.patch(
        url='/inks/update/588e7991-ccb1-481b-aa11-048a387744ab',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'brand': 'Solid Ink',
            'color': 'Magenta',
            'weight': '30ml'
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'ink not found'}


def test_delete_ink(client, session, user, token):
    ink = InkFactory.create(user_id=user.id)

    session.add(ink)
    session.commit()

    response = client.delete(
        url=f'/inks/delete/{ink.id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'detail': 'ink has been deleted'}


def test_delete_wrong_ink(client, token):
    response = client.delete(
        url='/inks/delete/588e7991-ccb1-481b-aa11-048a387744ab',
        headers={'Authorization': f'Bearer {token}'},
    )

    response.status_code == HTTPStatus.NOT_FOUND
    response.json() == {'detail': 'ink not found'}
