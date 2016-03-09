
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
                    conn.sendall(response_ok().encode('utf8'))
                    conn.close()
                    session_complete = True
    except KeyboardInterrupt:
        conn.close()
        server.close()


def response_ok():
    return """HTTP/1.1 200 OK\nContent-Type: text/plain\r\n"""


def response_error():
    return """HTTP/1.1 500 Internal Server Error\nContent-Type: text/plain\r\n"""

if __name__ == "__main__":
    # run this as script
    server()
