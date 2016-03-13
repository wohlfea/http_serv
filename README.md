Implements a simple server and client.

Server can parse good and bad http requests, and will return uri with http header to client.

On receiving a bad http request, server will return well-formatted http error code.

Server stays online, only excepting a keyboard interrupt. On keyboard interrupt, server diligently closes socket.

