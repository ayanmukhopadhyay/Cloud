# !/bin/python
from datetime import datetime
import BaseHTTPServer
import nova_server_create
from math import ceil

from fabric.api import env, execute, task
from fabric.operations import sudo, run, put

HOST = ''
PORT = 8080
vmName = 'ayan-ubuntu-test-vm'
global vmCounter = 1234

# fabric config
env.user = "ubuntu"
env.key_filename = "ayan_horizon.pem"

localVMs = []
global returnValue

@task
def copy():
    put('/home/ubuntu/checkPrime.py', '/home/ubuntu/')
    print "copied the file into newly created machine"

@task
def runPrimeCheck(n):
    returnValue = run("python checkPrime.py " + str(n))
    print returnValue

def send_req_to (vm, req):
    # get the timestamp
    t1 = datetime.now()

    # get the ip address from vm name
    env.hosts = nova_server_create.getLocalIPByServerName(vm)

    # send the req by using fabric
    execute(runPrimeCheck, req)

    # get the timestamp
    t2 = datetime.now()

    # return latency
    latency = t2 - t1
    return (returnValue, latency)

# MyHTTPHandler inherits from BaseHTTPServer.BaseHTTPRequestHandler
class MyHTTPHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET (s):
        """ Respond to a GET request. """
        print "GET request received; reading the request"
        # the parameter s is the "self" param
        # way to get hold of the path that was sent:
        path = s.path
        # using query string to send what we need
        number = int(path.split('?')[1].split('-')[0])
        method = path.split('?')[1].split('-')[1]
        if method == "isNumberPrime":
            pass
        else:
            print "Error: Bad request"
            s.send_response(400)

        # check the local server list, whether it's empty
        if not localVMs:
            # create one by using nova_server_create's new method
            nova_server_create.setup(primary = False, vmCounter)

            # copy the file checkPrime.py in the local VM
            execute(copy)

            # send the request to newly created local VM (also get the latency)
            isPrime, latency = send_req_to(vmName + str(vmCounter), number)

            vmCounter += 1

            # append the newly created VM's name and latency in the list
            localVMs.append([vmName + str(vmCounter), latency, time()])
        else:
            flag = False
            for localVM in localVMs:
                # search every VM which satisfies the criteria
                # i.e. check latency and last time stamp
                if (satisfies_criteria):
                    # send the request to this VM
                    isPrime, latency = send_req_to(localVM[0], number)

                    # update the latency, timestamp
                    localVM[1] = latency
                    localVM[2] = datetime.now()

                    # set the flag saying we got the method
                    flag = True
                    break

            # if there's no such machine
            if (!flag):
                # do everything which is upper if() - create a new one and stuff
                # create one by using nova_server_create's new method
                nova_server_create.setup(primary = False, vmCounter)

                # copy the file checkPrime.py in the local VM
                # get the ip address from vm name
                env.hosts = nova_server_create.getLocalIPByServerName(vmName + str(vmCounter))

                # copy the file by using fabric
                execute(copy)

                # send the request to newly created local VM (also get the latency)
                isPrime, latency = send_req_to(vmName + str(vmCounter), number)

                vmCounter += 1

                # append the newly created VM's name and latency in the list
                localVMs.append([vmName + str(vmCounter), latency, datetime.now()])


        s.send_response (200)
        s.send_header ("Content-type", "text/html")
        s.end_headers ()
        s.wfile.write ("<html><head><title>Title</title></head>")
        s.wfile.write ("<body><p>This is a test.</p>")
        s.wfile.write ("<p>Result is : %s</p>" % str(isPrime))
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


