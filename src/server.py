
# -*- coding: UTF-8 -*-
import socket
import os
import io
"""module docstring"""


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
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    try:
        server.bind(ADDRESS)
        server.listen(1)
        while True:
            conn = server.accept()[0]
            session_complete = False
            received_message = ''
            while not session_complete:
                part = conn.recv(BUFFER_LENGTH)
                received_message += part.decode('utf-8')
                if len(part) < BUFFER_LENGTH:
                    print('Request Received:')
                    print(received_message)
                    send_response(handled_request(received_message), conn)
                    conn.close()
                    session_complete = True
    except KeyboardInterrupt:
        conn.close()
    finally:
        server.close()


def handled_request(request):
    try:
        uri = parse_request(request)
        try:
            return response_ok(*resolve_uri(uri))
        except (OSError, IOError):
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
    if uri[-1] == u'/' and os.path.isdir(RESOURCES + uri):
        # TODO: If request only consists of a / send index.html
        dir_listing = u'<h1>Directory Listing</h1><ul>'
        for dirnames, subdirs, filenames in os.walk(RESOURCES + uri):
            for filename in filenames:
                dir_listing += u'<li>{}/{}</li>'.format(dirnames[11:-1], filename)
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
    except AssertionError:
        raise SyntaxError
    return uri


def response_ok(content_type, body):
    """Given body, and content type return formatted http response"""
    initial_header = u'HTTP/1.1 200 OK '
    content_type_header = u'Content-Type: {}\r\n'.format(content_type)
    response = [initial_header, content_type_header, body]
    return response


def response_error(error_type='500 Internal Server Error'):
    return [u"HTTP/1.1 {}".format(error_type)]


def send_response(response_list, conn):
    if not isinstance(response_list, list):
        print(response_list)
    for line in response_list:
        print(line)
        if isinstance(line, str):
            conn.send(line.encode('utf-8'))
        else:
            conn.send(line)


if __name__ == "__main__":
    # run this as script
    server()


# open all files (resources) as bytes
# catch all strings immediately before sending, and encode as bytes
# don't bother concating header lines with each other or with body
# send as series of lines (\r\n is implied when sending line by line)


