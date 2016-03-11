import pytest

DIR = [("GET img/ HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n",
        './image/image1.png')]


@pytest.mark.parametrize('req, result', DIR)
def test_directory(req, result):
    from client import client
    response = client(req)
    print(response)
    assert result in response
