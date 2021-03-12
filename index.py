# application module dependies
from Config.Config import *
from Utils.Utils import *
from Models.Models import *
from Controllers.Controllers import *
# application external dependies
import socket
import urllib
import json


# Create socket
server_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
server_socket.bind( ( Config.SERVER_HOST, Config.SERVER_PORT ) )
server_socket.listen( 1 )
print( 'Listening on port %s ...' % Config.SERVER_PORT )


while True:    


    # Wait for client connections
    client_connection, client_address = server_socket.accept()


    # Get the client request
    request = client_connection.recv( 4096 )

    request = HTTPRequest( request )

    print( 'req : ' + request.path )


    # CORS
    request.headers['Access-Control-Allow-Origin'] = '*' # rarther request.url
    request.headers['Access-Control-Allow-Headers'] = 'X-Requested-With'
    request.headers['Access-Control-Allow-Credentials'] = 'true'


    # Sanitize data & build context
    requestBody = request.rfile.read( int( request.headers['Content-Length'] ) )

    requestBody = json.loads( urllib.parse.unquote( requestBody ) )

    print( 'body : ' + json.dumps( requestBody ) )

    ctx = json.loads( json.dumps( requestBody['ctx'] ), object_hook=lambda d: globals()['Model' + requestBody['type']]( **d ) )

    requestBody['ctx'] = None

    api = json.loads( json.dumps( requestBody ), object_hook=lambda d: ModelApi( **d ) )

    api.ctx = ctx


    # Initalize Controller - Process Data
    controller = globals()['Controller' + requestBody['type']]

    interaction = getattr( controller, 'do' + api.interaction.title() )
    
    interaction( api )


    # Request Routing - Python 'Switch' Statement
    if request.command == 'POST':
        responseHeaders = 'HTTP/1.0 200 OK'
        responseBody = '\r\n\r\n200 OK\r\n'
    else:
        responseHeaders = 'HTTP/1.0 403 FORBIDDEN'
        responseBody = '\r\n\r\n403 FORBIDDEN\r\n'


    # Response
    for header in request.headers:
        if header != 'Content-Length':
            responseHeaders += '\r\n' + header + ': ' + request.headers[header]


    response = responseHeaders + responseBody


    # Send HTTP response
    print( 'res : ' + responseBody.strip() )
    print( ' ' )

    client_connection.sendall( response.encode() )
    client_connection.close()


# Close socket
server_socket.close()