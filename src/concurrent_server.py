from server import connection_handler

if __name__ == '__main__':
    """Wraps around connection_handler to handle multiple connections"""
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    patch_all()
    server = StreamServer(('127.0.0.1', 5000), connection_handler)
    print('Starting echo server on port 5000')
    server.serve_forever()
