import pytest


BAD_REQUEST_TEST_VALUES = [
    # bad methods - server only accepts GET
    ("POST /index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n",
     ValueError, 405),
    ("UPDATE /index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n",
     ValueError, 405),
    ("DELETE /index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n",
     ValueError, 405),
    ("/index.html HTTP/1.1\r\nHost: www.example.com\r\n\r\n",
     ValueError, 405),
    # bad protocol
    ("GET /index.html HTTP/1.0\r\nHost: www.example.com\r\n\r\n",
     NameError, 505),
    ("GET /index.html HTTP/1.2\r\nHost: www.example.com\r\n\r\n",
     NameError, 505),
    ("GET /index.html HTTP\2.0\r\nHost: www.example.com\r\n\r\n",
     NameError, 505),
    # bad host header
    ("GET /index.html HTTP/1.1\r\nHost www.example.com\r\n\r\n",
     SyntaxError, 400),
    ("GET /index.html HTTP/1.1\r\nHot: www.example.com\r\n\r\n",
     SyntaxError, 400),
    ("GET /index.html HTTP/1.1\r\nHot: www.exa mple.com\r\n\r\n",
     SyntaxError, 400),
]
GOOD_REQUEST_TEST_VALUES = [
    ("GET /index.html HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n",
     '/index.html'),
    ("GET /potato/index.html HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n",
     '/potato/index.html'),
    ("GET /index.html HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n",
     '/index.html'),
    ("GET /index.html HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n",
     '/index.html'),
    ("GET /index.html HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n",
     '/index.html'),
]


@pytest.mark.parametrize('args, result, http_error_code',
                         BAD_REQUEST_TEST_VALUES)
def test_bad_http_request(args, result, http_error_code):
    from server import parse_request
    with pytest.raises(result):
        parse_request(args)


@pytest.mark.parametrize('args, result', GOOD_REQUEST_TEST_VALUES)
def test_good_http_request(args, result):
    from server import parse_request
    assert parse_request(args) == result


@pytest.mark.parametrize('args, result', GOOD_REQUEST_TEST_VALUES)
def test_good_client_request(args, result):
    from client import client
    assert result in client(args)


@pytest.mark.parametrize('args, result, http_error_code',
                         BAD_REQUEST_TEST_VALUES)
def test_bad_client_request(args, result, http_error_code):
    from client import client
    assert str(http_error_code) in client(args)
