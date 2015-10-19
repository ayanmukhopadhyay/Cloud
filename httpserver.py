# !/bin/python
from datetime import datetime
import BaseHTTPServer
from nova_server_create import setup, getLocalIPByServerName
import subprocess

from fabric.api import env, execute, task
from fabric.operations import sudo, run, put
from fabric.api import run, sudo, local, env
import paramiko
import socket

HOST = ''
PORT = 8080
vmName = 'ayan-ubuntu-test-vm'
vmCounter = 1234

def _is_host_up(host, port):
    # Set the timeout
    original_timeout = socket.getdefaulttimeout()
    new_timeout = 3
    socket.setdefaulttimeout(new_timeout)
    host_status = False
    try:
        transport = paramiko.Transport((host, port))
        host_status = True
    except:
        print('***Warning*** Host {host} on port {port} is down.'.format(
            host=host, port=port)
        )
    socket.setdefaulttimeout(original_timeout)
    return host_status

# fabric config
env.user = "ubuntu"
env.key_filename = "ayan_horizon.pem"
env.skip_bad_hosts = True

localVMs = []
returnValue = None

@task
def copy():
    put('/home/ubuntu/checkPrime.py', '/home/ubuntu/')
    print "copied the file into newly created machine"

@task
def runPrimeCheck(n):
    returnValue = run("python checkPrime.py " + str(n))
    print returnValue

def spawnVM(self,counter):
    setup(primary=False,counter=counter)

'''
def workWithLatency(self,latency):
    latencyRecord.append(latency)
    if len(latencyRecord) > 2:
        averageLatency=sum(latencyRecord[0:len(latencyRecord)-2])/float(len(len(latencyRecord)-2))#calculate average latency
        if (latency-averageLatency)/float(averageLatency)*100 > 20:#check how much latency has risen in percentage
            self.spawnVM(vmCounter+1)
'''
def send_req_to (vm, req):
    # get the timestamp
    t1 = datetime.now()

    # get the ip address from vm name
    vm_ip = getLocalIPByServerName(vm)

    # send the req by using fabric
    command = "python runCheckPrime.py " + vm_ip + " " + req
    print "command to run: " + command
    process = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
    output = process.communicate()[0]
    from time import sleep
    while True:
        print "output: " + str(output)
        sleep(5)

    # get the timestamp
    t2 = datetime.now()

    # return latency
    latency = t2 - t1
    return (returnValue, latency)

# MyHTTPHandler inherits from BaseHTTPServer.BaseHTTPRequestHandler
class MyHTTPHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET (s):
        global vmCounter
        """ Respond to a GET request. """
        print "GET request received; reading the request"
        # the parameter s is the "self" param
        # way to get hold of the path that was sent:
        path = s.path
        # using query string to send what we need
        number = int(path.split('?')[1].split('-')[0])
        method = path.split('?')[1].split('-')[1]
        # content_length = int(s.headers['Content-length'])
        # number = int(s.rfile.read(content_length))
        # method = "isNumberPrime"
        if method == "isNumberPrime":
            pass
        else:
            print "Error: Bad request"
            s.send_response(400)

        # check the local server list, whether it's empty
        if not localVMs:
            # create one by using nova_server_create's new method
            setup(primary = False, counter = vmCounter)
            print "Local VM " + str(getLocalIPByServerName(vmName + str(vmCounter))) + " is created"

            #TODO: change the known_hosts file
            # command = "ssh-keyscan -t rsa,dsa " + getLocalIPByServerName(vmName + str(vmCounter)) + " 2>&1 | sort -u - ~/.ssh/known_hosts > ~/.ssh/tmp_hosts"
            # print "command to run: " + command
            # process = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
            # output = process.communicate()[0]
            # print "output: " + output
            # command = "mv ~/.ssh/tmp_hosts ~/.ssh/known_hosts"
            command = "ssh-keyscan " + getLocalIPByServerName(vmName + str(vmCounter)) + " >> ~/.ssh/known_hosts"
            print "command to run: " + command
            process = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
            output = process.communicate()[0]
            print "output: " + output

            # copy the file checkPrime.py in the local VM
            # set environment
            # env.hosts = ["ubuntu@" + str(getLocalIPByServerName(vmName + str(vmCounter))),]
            # print env.hosts
            # while True:
            #     if _is_host_up(env.hosts[0],22):
            #         execute(copy)
            #         break
            # command = "ssh -i ayan_horizon.pem ubuntu@" + getLocalIPByServerName(vmName + str(vmCounter))
            command = "python copyCheckPrime.py " + getLocalIPByServerName(vmName + str(vmCounter))
            print "command to run: " + command
            process = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
            output = process.communicate()[0]
            # from time import sleep
            # while True:
            #     print "output: " + str(output)
            #     sleep(5)

            # send the request to newly created local VM (also get the latency)
            isPrime, latency = send_req_to(vmName + str(vmCounter), str(number))

            vmCounter += 1

            # append the newly created VM's name and latency in the list
            localVMs.append([vmName + str(vmCounter), latency, datetime.now()])
        else:
            flag = False
            for localVM in localVMs:
                # search every VM which satisfies the criteria
                # i.e. check latency and last time stamp
                #TODO: Get rid of satisfies_criteria
                satisfies_criteria = True
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
            if (not flag):
                # do everything which is upper if() - create a new one and stuff
                # create one by using nova_server_create's new method
                setup(primary = False, counter=vmCounter)

                # copy the file checkPrime.py in the local VM
                # get the ip address from vm name
                env.hosts = getLocalIPByServerName(vmName + str(vmCounter))

                # copy the file by using fabric
                execute(copy)

                # send the request to newly created local VM (also get the latency)
                isPrime, latency = send_req_to(vmName + str(vmCounter), number)

                vmCounter += 1

                # append the newly created VM's name and latency in the list
                localVMs.append([vmName + str(vmCounter), latency, datetime.now()])

        if method=="isNumberPrime":
            s.send_response (200)
            s.send_header ("Content-type", "text/html")
            s.end_headers ()
            s.wfile.write ("<html><head><title>Title</title></head>")
            s.wfile.write ("<body><p>This is a test.</p>")
            s.wfile.write ("<p>Result is : %s</p>" % str(isPrime))
            s.wfile.write ("</body.<html>")



if __name__ == '__main__':
    print "Populating current localVMs directory"
    #TODO: Populate localVMs directory to get the already existing VMs - set latency and last time to zero

    print "Instantiating a BaseHTTPServer"
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class ((HOST, PORT), MyHTTPHandler)
    try:
        print "Run a BaseHTTPServer"
        httpd.serve_forever ()
    except KeyboardInterrupt:
        pass

    httpd.server_close ()


