import pytest


DIR = [
    (u"GET /img/ HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n",
     [u'HTTP/1.1 200 OK',
      u'Content-Type: text/html',
      u'',
      u'<h1>Directory Listing</h1><ul><li>/img/catburrito.jpg</li><li>/img/image1.png</li><li>/img/image2.jpg</li></ul>']),
]
HANDLED_REQUEST_ARGS = [
    (SyntaxError, )
]
ERROR_ARGS = [
    ('none', 'HTTP/1.1 500 Internal Server Error')
]
URI_ARGS = [
    ('/img/', 'text/html',
     '<h1>Directory Listing</h1><ul><li>/img/catburrito.jpg</li><li>/img/image1.png</li><li>/img/image2.jpg</li></ul>'),
    ('/index.html', 'text/html',
     b'<h1>THIS IS THE INDEX FILE</h1>\n<a href=\'/\'>Click here for a directory listing</a>\n')
]
BAD_URI_ARGS = [
    ('/bad_dir/', (IOError, OSError)),
]


@pytest.mark.parametrize('req, expected_response', DIR)
def test_directory_request(req, expected_response):
    from client import client
    actual_response = client(req)
    assert isinstance(actual_response, str)
    for line in expected_response:
        assert line in actual_response


@pytest.mark.parametrize('uri, content_type, body', URI_ARGS)
def test_resolve_uri(uri, content_type, body):
    from server import resolve_uri
    assert resolve_uri(uri) == (content_type, body)


@pytest.mark.parametrize('uri, returned_error', BAD_URI_ARGS)
def test_resolve_uri_bad_input(uri, returned_error):
    from server import resolve_uri
    with pytest.raises(returned_error):
        resolve_uri(uri)


@pytest.mark.parametrize('error_type, response', ERROR_ARGS)
def test_response_error(error_type, response):
    from server import response_error
    assert response_error()[0] == response


def test_response_error_return_length():
    from server import response_error
    assert len(response_error()) == 2


def test_response_ok_return_type():
    from server import response_ok
    assert isinstance(response_ok(u'text/plain', u'this is a body'), list)


def test_response_ok_return_length():
    from server import response_ok
    assert len(response_ok(u'text/html', u'this is a body')) == 4


def test_response_ok_list_types():
    from server import response_ok
    for line in response_ok(u'image/jpeg', u''):
        assert isinstance(line, str)
