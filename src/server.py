import socket
"""module docstring"""


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5000)
    server.bind(address)
    # start server running
    server.listen(1)
    conn, addr = server.accept()
    # send responses to any received messages
    # can cleanly exit on ctrl-d
    # all sockets should be closed on exit
    pass

if __name__ == "__main__":
    # TODO
    # run this as script
    server()
