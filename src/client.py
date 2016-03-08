import socket
"""module docstring"""


def client(message):
    """function doctstring"""
    # retrieve list of comm profiles at given socket
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    # select SOCK_STREAM comm profile
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    # instantiate client socket with matching comm profile
    client = socket.socket(*stream_info[:3])
    # connect to server socket (given by param)
    client.connect(stream_info[-1])
    # send message


    client.sendall(message.encode('utf8'))

    buffer_length = 1024
    reply_complete = False
    received_message = ''
    while not reply_complete:
        part = client.recv(buffer_length)
        received_message += part.decode('utf8')
        if len(part) < buffer_length and received_message != '':
            client.close()
            return received_message

    # accumulate any reply sent by server into string
    # when full reply received, close socket
    # return message
    # print(stream_info)
    # return infos

    # open a socket connection to server
    # send message passed as argument to server via socket

if __name__ == "__main__":
    # run this as script
    client("mmessagemessageessage")
