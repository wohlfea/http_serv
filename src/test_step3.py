import pytest



DIR = [
    (u"GET /img/ HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n",
     u'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Directory Listing</h1><ul><li>/img/catburrito.jpg</li><li>/img/image1.png</li><li>/img/image2.jpg</li></ul>\r\n'),
]
HANDLED_REQUEST_ARGS = [
    (SyntaxError, )
]
ERROR_ARGS = [
    ('none', 'HTTP/1.1 500 Internal Server Error\r\n\r\n')
]
URI_ARGS = [
    ('/img/', 'text/html',
     '<h1>Directory Listing</h1><ul><li>/img/catburrito.jpg</li><li>/img/image1.png</li><li>/img/image2.jpg</li></ul>'),
    ('/index.html', 'text/html',
     '<h1>THIS IS THE INDEX FILE</h1>\n<a href=\'directory/\'>Click here for a directory listing</a>\n')
]
BAD_URI_ARGS = [
    ('/bad_dir/', (IOError, OSError)),
]


@pytest.mark.parametrize('req, result', DIR)
def test_directory_request(req, result):
    from client import client
    response = client(req)
    assert result == response


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
    assert response_error() == response
