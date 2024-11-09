from jwt import decode

from inkmanager.security import SECRET_KEY, create_access_token


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data=data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])
    assert decoded['test'] == data['test']
    assert decoded['exp']
