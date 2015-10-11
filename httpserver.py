# !/bin/python
import time
import BaseHTTPServer
from math import ceil
from nova_server_create import setup

HOST = ''
PORT = 8080
vmCounter=1
latencyRecord=[]

# MyHTTPHandler inherits from BaseHTTPServer.BaseHTTPRequestHandler
class MyHTTPHandler (BaseHTTPServer.BaseHTTPRequestHandler):

    def isNumberPrime(self,number):
        for counter in range(2,int(ceil(number/2))):
            if number%counter == 0:
                return False
        return True

    def spawnVM(self,counter):
        setup(primary=False,counter=counter)

    def workWithLatency(self,latency):
        latencyRecord.append(latency)
        if len(latencyRecord) > 2:
            averageLatency=sum(latencyRecord[0:len(latencyRecord)-2])/float(len(len(latencyRecord)-2))#calculate average latency
            if (latency-averageLatency)/float(averageLatency)*100 > 20:#check how much latency has risen in percentage
                self.spawnVM(vmCounter+1)


    def do_GET (s):
        """ Respond to a GET request. """
        print "GET request received; reading the request"
        # the parameter s is the "self" param
        #way to get hold of the path that was sent:
        path = s.path
        # #using query string to send what we need
        number = int(path.split('?')[1].split('-')[0])
        method = path.split('?')[1].split('-')[1]
        if method=="isNumberPrime":
            isPrime = s.isNumberPrime(number)
            s.send_response (200)
            s.send_header ("Content-type", "text/html")
            s.end_headers ()
            s.wfile.write ("<html><head><title>Title</title></head>")
            s.wfile.write ("<body><p>This is a test.</p>")
            s.wfile.write ("<p>Result is : %s</p>" % str(isPrime))
            s.wfile.write ("</body.<html>")
        if method=="latencyReport":
            number = int(path.split('?')[1].split('-')[0])
            s.send_response(200)
            s.send_header ("Content-type", "text/html")
            s.end_headers ()
            s.wfile.write ("<html><head><title>Title</title></head>")
            s.wfile.write ("<body><p>This is a test.</p>")
            s.wfile.write ("</body.<html>")

            s.workWithLatency(number)



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


