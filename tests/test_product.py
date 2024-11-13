from http import HTTPStatus

from .factories import ProductFactory


def test_create_product(client, token, user):
    amount = 12
    user_id = str(user.id)
    response = client.post(
        url='/products/create',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Bandagem p/ máquina de tattoo',
            'amount': amount,
            'user_id': user_id,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Bandagem p/ máquina de tattoo'
    assert response.json()['amount'] == amount


def test_get_product_by_id(client, session, user, token):
    product = ProductFactory.create(user_id=user.id)

    session.add(product)
    session.commit()

    response = client.get(
        url=f'/products/product/{product.id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == str(product.id)


def test_get_inexistent_product_by_(client, token):
    response = client.get(
        url='/products/product/588e7991-ccb1-481b-aa11-048a387744ab',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'product not found'}


def test_list_products(client, session, user):
    expected_products = 3
    session.bulk_save_objects(ProductFactory.create_batch(3, user_id=user.id))
    session.commit()

    response = client.post(
        url='/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.OK
    token = response.json()['access_token']

    response = client.get(
        url='/products', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['products']) == expected_products


def test_list_products_should_return_10(client, user, token, session):
    expected = 10

    session.bulk_save_objects(ProductFactory.create_batch(20, user_id=user.id))
    session.commit()

    response = client.get(
        url='/products/?offset=1&limit=10',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['products']) == expected


def test_list_products_by_name_should_return_7(client, user, token, session):
    expected = 7

    for i in range(expected):
        product = ProductFactory.create(
            name=f'Bandagem {i}', amount=12, user_id=user.id
        )
        session.add(product)
        session.commit()

    response = client.get(
        url='/products/?name=bandagem',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['products']) == expected


def test_change_product_amount_value(client, session, user, token):
    product = ProductFactory.create(user_id=user.id)

    session.add(product)
    session.commit()

    amount = 2

    response = client.patch(
        url=f'/products/update/{product.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'amount': amount},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['amount'] == amount


def test_change_wrong_product(client, token):
    amount = 2

    response = client.patch(
        url='/products/update/588e7991-ccb1-481b-aa11-048a387744ab',
        headers={'Authorization': f'Bearer {token}'},
        json={'amount': amount},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'product not found'}


def test_delete_product(client, session, user, token):
    product = ProductFactory.create(user_id=user.id)

    session.add(product)
    session.commit()

    response = client.delete(
        url=f'/products/delete/{product.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'detail': 'product has been deleted'}


def test_delete_wrong_product(client, token):
    response = client.delete(
        url='/products/delete/588e7991-ccb1-481b-aa11-048a387744ab',
        headers={'Authorization': f'Bearer {token}'},
    )

    response.status_code == HTTPStatus.NOT_FOUND
    response.json() == {'detail': 'product not found'}
