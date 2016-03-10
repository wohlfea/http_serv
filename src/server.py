
# -*- coding: UTF-8 -*-
import socket
"""module docstring"""


BUFFER_LENGTH = 1024
ADDRESS = ('127.0.0.1', 5000)


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
        server.close()


def handled_request(request):
    try:
        uri = parse_request(request)
        return response_ok() + uri
    except SyntaxError:
        return response_error('400 Bad Request')
    except ValueError:
        return response_error('405 Method Not Allowed')
    except NameError:
        return response_error('505 HTTP Version Not Supported')
    else:
        return response_error()


def parse_request(http_request):
    try:
        request_list = http_request.split('\r\n')
        # assert len(request_list) >= 2
        line_1 = request_list[0]
        method, uri, protocol = line_1.split()
        assert method == u'GET'
    except:
        raise ValueError
    try:
        assert protocol == u'HTTP/1.1'
    except:
        raise NameError
    try:
        host_header = request_list[1]
        assert host_header[:5] == 'Host:'
        assert len(host_header.split()) == 2
    except:
        raise SyntaxError
    return uri


def response_ok():
    return """HTTP/1.1 200 OK\nContent-Type: text/plain\r\n\r\n"""


def response_error(error_type='500 Internal Server Error'):
    return u"HTTP/1.1 {}\r\n\r\n".format(error_type)


if __name__ == "__main__":
    # run this as script
    server()
