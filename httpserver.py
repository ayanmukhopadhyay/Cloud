# !/bin/python
from datetime import datetime
import BaseHTTPServer
from nova_server_create import setup, getLocalIPByServerName, bringVMFromPool
import subprocess
from itertools import cycle
import numpy as np

from fabric.api import env, execute, task
from fabric.operations import sudo, run, put
from fabric.api import run, sudo, local, env
import paramiko
import socket

HOST = ''
PORT = 8080
vmName = 'ayan-ubuntu-test-vm'
#vmCounter = 1234
vmDomain = [["ayan-ubuntu-test-vm-worker-1","10.10.3.204"],["ayan-ubuntu-test-vm-worker-2","10.10.3.205"],["ayan-ubuntu-test-vm-worker-3","10.10.3.206"]]
reqCounter=0#track number of requests to sleep

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

localVMs = {}
vmList = []#stores only names
vmListCycle = cycle(vmList)
returnValue = None
loadBalancingStrategy = "roundRobin"
#loadBalancingStrategy = "waitedPolling"

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
def send_req_to (vm, req, reqCounter):
    # get the timestamp
    t1 = datetime.now()

    # get the ip address from vm name
    vm_ip = getLocalIPByServerName(vm)
    print vm_ip
    # send the req by using fabric
    command = "python runCheckPrime.py " + str(vm_ip) + " " + req + " " + str(reqCounter)
    print "command to run: " + command
    process = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
    output = process.communicate()[0]
    print output
    output = output.split('@')[1]
    print output

    # from time import sleep
    # while True:
    #     print "output: " + str(output)
    #     sleep(5)

    # get the timestamp
    t2 = datetime.now()

    # return latency
    latency = (t2 - t1).total_seconds()
    return (output, latency)

def plotLatency():
    latencies = []#will store datetime and latency values in a 2d array
    for key,value in localVMs.iteritems():
        if len(latencies) == 0:
            latencies.append(value[0])#update latencies
            latencies.append(value[1])#update datetimes
        else:
            latencies[0].extend(value[0])
            latencies[1].extend(value[1])
    #sort according to time as different vms were spawned at different times
    latencies = np.array(latencies)
    latencies = latencies[np.argsort(latencies[:,1])]
    np.save("latencies",latencies)




# MyHTTPHandler inherits from BaseHTTPServer.BaseHTTPRequestHandler
class MyHTTPHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET (s):
        global vmCounter
        global reqCounter
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
            reqCounter+=1
            pass
        else:
            print "Error: Bad request"
            s.send_response(400)

        # check the local server list, whether it's empty
        if not localVMs:
            print "local vm doesnt exist"
            # create one by using nova_server_create's new method
            #setup(primary = False, counter = vmCounter)
            vm = bringVMFromPool(vmDomain,vmList)
            print vm
            if vm != None:
                vmList.append(vm[0])
                print "Local VM " + str(vm[1]) + " is created"
            '''
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
            '''
            # copy the file checkPrime.py in the local VM
            # set environment
            # env.hosts = ["ubuntu@" + str(getLocalIPByServerName(vmName + str(vmCounter))),]
            # print env.hosts
            # while True:
            #     if _is_host_up(env.hosts[0],22):
            #         execute(copy)
            #         break
            # command = "ssh -i ayan_horizon.pem ubuntu@" + getLocalIPByServerName(vmName + str(vmCounter))
            #command = "python copyCheckPrime.py " + getLocalIPByServerName(vmName + str(vmCounter))
            #command = "python copyCheckPrime.py " + getLocalIPByServerName(vm[0])
            command = "python copyCheckPrime.py " + str(vm[1])
            print "command to run: " + command
            process = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
            output = process.communicate()[0]
            # from time import sleep
            # while True:
            #     print "output: " + str(output)
            #     sleep(5)

            # send the request to newly created local VM (also get the latency)
            isPrime, latency = send_req_to(vm[0], str(number),reqCounter)
            #vmList.append(vm[0])

            #vmCounter += 1

            # append the newly created VM's name and latency in the list
            #localVMs.update({vmName + str(vmCounter): [[latency], [datetime.now()]]})
            localVMs.update({vm[0]: [[latency], [datetime.now()]]})
        else:
            print "local vm exists"
            #flag = False
            machineToPing = s.getMachineToPing(loadBalancingStrategy)
            print machineToPing
            if machineToPing != -1:
                #for localVM in localVMs:

                    # search every VM which satisfies the criteria
                    # i.e. check latency and last time stamp
                    # satisfies_criteria = True
                    # if (satisfies_criteria):
                        # send the request to this VM
                isPrime, latency = send_req_to(machineToPing, str(number), reqCounter)

                # update the latency, timestamp
                localVMs[machineToPing][0].append(latency)
                localVMs[machineToPing][1].append(datetime.now())

                        # localVM[1] = latency
                        # localVM[2] = datetime.now()
                        # set the flag saying we got the method
                        # flag = True
                        # break
            else:#didnt find a good vm. must spawn another
            # if there's no such machine
            # if (not flag):
                # do everything which is upper if() - create a new one and stuff
                # create one by using nova_server_create's new method
                #setup(primary = False, counter=vmCounter)
                print "Domain is " + str(vmDomain)
                print "List is " + str(vmList)
                vm = bringVMFromPool(vmDomain,vmList)
                if vm != None:
                    vmList.append(vm)
                    print "Local VM " + str(vm[0]) + " is created"
                    #env.hosts = getLocalIPByServerName(vmName + str(vmCounter))
                    #execute(copy)
                    isPrime, latency = send_req_to(vm, str(number), reqCounter)
                    localVMs.update({vm[0]: [[latency], [datetime.now()]]})
                else:
                    #we wanted a new VM but we have exceeded capacity
                    isPrime, latency = send_req_to(vmList[0], str(number), reqCounter)
                    localVMs.update({vm[0]: [[latency], [datetime.now()]]})



                '''
                # copy the file checkPrime.py in the local VM
                # get the ip address from vm name
                env.hosts = getLocalIPByServerName(vmName + str(vmCounter))

                # copy the file by using fabric
                execute(copy)

                # send the request to newly created local VM (also get the latency)
                #isPrime, latency = send_req_to(vmName + str(vmCounter), number)
                isPrime, latency = send_req_to(vm, number)

                vmCounter += 1

                # append the newly created VM's name and latency in the list
                localVMs.update({vmName + str(vmCounter): [[latency], [datetime.now()]]})
                #localVMs.append([vmName + str(vmCounter), latency, datetime.now()])
                '''
        if method=="isNumberPrime":
            s.send_response (200)
            s.send_header ("Content-type", "text/html")
            s.end_headers ()
            s.wfile.write ("<html><head><title>Title</title></head>")
            s.wfile.write ("<body><p>This is a test.</p>")
            s.wfile.write ("<p>Result is : %s</p>" % str(isPrime))
            s.wfile.write ("</body.<html>")

    def getMachineToPing(s,strategy):
        print localVMs
        found = False # can we find even 1 okay VM?
        for key,value in localVMs.iteritems():
            lastLatency = value[0][-1]
            print lastLatency
            if lastLatency < 5:
                found = True# found one okay VM. No need to spawn another. Implement strategy
        if strategy == "roundRobin":
            if found:
                return next(vmListCycle)#do round robin
        if strategy == "waitedPolling":
            if found:
                return vmList[s.getLeastCurrentLatency()]
        if not found:
            return -1


    def waitedPollingStrategy(self):
        lastLatencies = []
        lastPolled = []
        for key, value in localVMs.iteritems():
            lastLatencies.append(value[0][-1]) #get the last latency from this VM
            lastPolled.append(value[1][-1])#get the last polled date from this VM
        #if VMs havent been polled for a minute, poll it once to update latency and see whats happennning
        diffLastPolled = [abs(datetime.Now - lastPolledTime).total_seconds() for lastPolledTime in lastPolled]#find time since last Polled
        if max(diffLastPolled) > 30:
            return diffLastPolled.index(max(diffLastPolled))
        else: #all vms have been spawned recently. Pick the VM with least latency
            return lastLatencies.index(min(lastLatencies))

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


