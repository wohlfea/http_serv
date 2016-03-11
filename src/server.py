
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
                received_message += part.decode('utf8')
                if len(part) < BUFFER_LENGTH:
                    print('Request Received:')
                    print(received_message)
                    conn.sendall(handled_request(received_message).encode('utf8'))
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
    if uri[-1] == u'/':
        #TODO: Test wether directory exists
        #TODO: If request only consists of a / send index.html
        dir_listing = u'<h1>Directory Listing</h1><ul>'
        for dirnames, subdirs, filenames in os.walk(RESOURCES):
            for filename in filenames:
                dir_listing += u'<li>{}/{}</li>'.format(dirnames, filename)
        dir_listing += u'</ul>'
        content_type = 'text/html'
        body = dir_listing
    else:
        content_type = EXTENSION_DICT[uri.split('.')[-1]]
        print(RESOURCES+uri)
        with io.open(RESOURCES+uri, 'r') as data:
            body = data.read()
    return content_type, body


def parse_request(http_request):
    try:
        request_list = http_request.split('\r\n')
        # assert len(request_list) >= 2
        line_1 = request_list[0]
        method, uri, protocol = line_1.split()
        print(method, uri, protocol)
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
    return 'HTTP/1.1 200 OK\nContent-Type: {}\r\n\r\n{}\r\n'.format(content_type, body)


def response_error(error_type='500 Internal Server Error'):
    return u"HTTP/1.1 {}\r\n\r\n".format(error_type)


if __name__ == "__main__":
    # run this as script
    server()
