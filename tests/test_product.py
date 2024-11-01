from http import HTTPStatus


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
    ...
