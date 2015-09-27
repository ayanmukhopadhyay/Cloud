# !/bin/python
import time
import BaseHTTPServer

HOST = ''
PORT = 8080

# MyHTTPHandler inherits from BaseHTTPServer.BaseHTTPRequestHandler
class MyHTTPHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET (s):
        """ Respond to a GET request. """
        print "GET request received; reading the request"
        # the parameter s is the "self" param
        req = s.rfile.readline ()
        print "Received request = ", req
        s.send_response (200)
        s.send_header ("Content-type", "text/html")
        s.end_headers ()
        s.wfile.write ("<html><head><title>Title</title></head>")
        s.wfile.write ("<body><p>This is a test.</p>")
        s.wfile.write ("<p>You accessed path: %s</p>" % s.path)
        s.wfile.write ("</body.<html>")


if __name__ == '__main__':
    print "Instantiating a BaseHTTPServer"
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class ((HOST, PORT), MyHTTPHandler)
    try:
        print "Run a BaseHTTPServer"
        httpd.serve_forever ()
    except KeyboardInterrupt:
        pass

    httpd.server_close ()


