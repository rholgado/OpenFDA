import socketserver
import web

##
##WEB server
##

PORT=8000

socketserver.TCPServer.allow_reuse_address=True

# Handler = http.server.SimpleHTTPRequestHandler
Handler = web.testHTTPRequestHandler

httpd = socketserver.TCPServer(("",PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
