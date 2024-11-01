from http import HTTPStatus

from tests.factories import ProductFactory


def test_create_product(client):
    amount = 12
    response = client.post(
        '/products/create',
        json={'name': 'Bandagem p/ máquina de tattoo', 'amount': amount},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'Bandagem p/ máquina de tattoo'
    assert response.json()['amount'] == amount


def test_list_products(client, session):
    expected_products = 3
    session.bulk_save_objects(ProductFactory.create_batch(3))
    session.commit()

    response = client.get('/products')

    assert len(response.json()['products']) == expected_products


def test_change_product_amount(client, session):
    product = ProductFactory()

    session.add(product)
    session.commit()

    amount = 2

    response = client.patch(
        f'/products/update/{product.id}',
        json={
            'amount': amount
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['amount'] == amount


def test_delete_product(client, session):
    product = ProductFactory()

    session.add(product)
    session.commit()

    response = client.delete(f'/products/delete/{product.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'detail': 'task has been deleted successful'}
