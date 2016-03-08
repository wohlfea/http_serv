import socket
"""module docstring"""


def client(message):
    """function doctstring"""
    # open a socket connection to server
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    # send message passed as argument to server via socket
    # accumulate any reply sent by server into string
    # when full reply received, close socket
    # return message
    print(message)
    pass

if __name__ == "__main__":
    # TODO
    # run this as script
    pass
