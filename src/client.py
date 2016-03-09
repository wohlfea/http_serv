
# -*- coding: UTF-8 -*-
import socket
"""Simple client to send and receive echo"""


BUFFER_LENGTH = 1024
ADDRESS = ('127.0.0.1', 5000)


def client(message):
    """function doctstring"""
    # retrieve list of comm profiles at given socket
    infos = socket.getaddrinfo(*ADDRESS)
    # select SOCK_STREAM comm profile
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    # instantiate client socket with matching comm profile
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    client.sendall(message.encode('utf8'))
    # after sending message, close socket for writing and send empty byte
    client.shutdown(socket.SHUT_WR)
    received_message = ''
    while True:
        part = client.recv(BUFFER_LENGTH)
        received_message += part.decode('utf8')
        if len(part) < BUFFER_LENGTH:
            client.close()
            return received_message


if __name__ == "__main__":
    # run this as script
    client("mmessagemessageessage")
