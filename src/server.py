
# -*- coding: UTF-8 -*-
import socket
import os
import io


BUFFER_LENGTH = 1024
ADDRESS = ('127.0.0.1', 5000)
RESOURCES = './resources'
EXTENSION_DICT = {
    'html': 'text/html',
    'txt': 'text/plain',
    'jpg': 'image/jpeg',
    'png': 'image/png',
    'js': 'application/javascript',
    'css': 'text/css',
    'ico': 'image/x-icon',
    'svg': 'image/svg+xml',
}


def server():
    """Create server to receive http requests and send http responses"""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    try:
        server.bind(ADDRESS)
        server.listen(1)
        listening = True
        while listening:
            conn = server.accept()[0]
            connection_handler(conn, ADDRESS)
    except KeyboardInterrupt:
        try:
            conn.close()
        except UnboundLocalError:
            pass
    finally:
        server.close()


def connection_handler(conn, ADDRESS):
    """Receive message, respond, and close connection"""
    session_complete = False
    received_message = u''
    while not session_complete:
        part = conn.recv(BUFFER_LENGTH)
        received_message += part.decode('utf-8')
        if len(part) < BUFFER_LENGTH:
            print('Request Received:')
            print(received_message)
            send_response(handled_request(received_message), conn)
            session_complete = True
            conn.close()


def handled_request(request):
    """Determine validity of request, returning http responses as appropriate"""
    try:
        uri = parse_request(request)
        try:
            return response_ok(*resolve_uri(uri))
        except (OSError, IOError, KeyError):
            return response_error(u'404 Not Found')
    except SyntaxError:
        return response_error(u'400 Bad Request')
    except ValueError:
        return response_error(u'405 Method Not Allowed')
    except NameError:
        return response_error(u'505 HTTP Version Not Supported')
    else:
        return response_error()


def resolve_uri(uri):
    """Given uri, return local resource"""
    if uri[-1] == u'/' and os.path.isdir(RESOURCES + uri):
        # TODO: If request only consists of a / send index.html
        dir_listing = u'<h1>Directory Listing</h1><ul>'
        for dirnames, subdirs, filenames in os.walk(RESOURCES + uri):
            for filename in filenames:
                dir_listing += u'<li>{}/{}</li>'.format(dirnames[11:-1],
                                                        filename)
        dir_listing += u'</ul>'
        content_type = 'text/html'
        body = dir_listing
    elif uri[-1] == u'/' and not os.path.isdir(RESOURCES + uri):
        raise IOError
    # io.open throws IOError on bad filename
    else:
        content_type = EXTENSION_DICT[uri.split('.')[-1]]
        with io.open(RESOURCES + uri, 'rb') as data:
            body = data.read()
    return content_type, body


def parse_request(http_request):
    """Parses http request, returning uri and raising errors on bad requests"""
    try:
        request_list = http_request.split('\r\n')
        # assert len(request_list) >= 2
        line_1 = request_list[0]
        method, uri, protocol = line_1.split()
        assert method == u'GET'
    except AssertionError:
        raise ValueError
    try:
        assert protocol == u'HTTP/1.1'
    except AssertionError:
        raise NameError
    try:
        host_header = request_list[1]
        assert host_header[:5] == 'Host:'
        assert len(host_header.split()) == 2
    except (AssertionError, IndexError):
        raise SyntaxError
    return uri


def response_ok(content_type, body):
    """Return formatted http response"""
    initial_header = u'HTTP/1.1 200 OK'
    content_type_header = u'Content-Type: {}'.format(content_type)
    response = [initial_header, content_type_header, u'', body]
    return response


def response_error(error_type='500 Internal Server Error'):
    """Return formatted http response error"""
    return [u"HTTP/1.1 {}".format(error_type), '']


def send_response(response_list, conn):
    """Send http response, one line at a time, encoding as necessary"""
    for line in response_list:
        if isinstance(line, str):
            conn.send(line.encode('utf-8'))
        else:
            conn.send(line)


if __name__ == "__main__":
    server()
