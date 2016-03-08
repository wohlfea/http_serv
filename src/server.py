import socket
"""module docstring"""


def server():
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    try:
        address = ('127.0.0.1', 5000)
        server.bind(address)
        # start server running
        while True:
            server.listen(1)
            conn, addr = server.accept()
            # send responses to any received messages
            buffer_length = 1024
            session_complete = False
            received_message = ''
            while not session_complete:
                part = conn.recv(buffer_length)
                received_message += part.decode('utf8')
                if len(part) < buffer_length and received_message != '':
                    conn.sendall(received_message.encode('utf8'))
                    received_message = ''
                    conn.close()
                    session_complete = True
    # DONE all sockets should be closed on exit
    except KeyboardInterrupt:
        conn.close()
        server.close()


if __name__ == "__main__":
    # run this as script
    server()
