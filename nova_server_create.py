#!/usr/bin/env python
import os
import sys
import time
from novaclient.v2 import client

secondaryVMCounter = 0

# Institution: Vanderbilt University
# Code created for the CS4287-5287 course
# Author: Aniruddha Gokhale
# Created: Fall 2015

# The purpose of this code is to show how to create a server using the nova API.

# get our credentials from the environment variables
def get_nova_creds ():
    d = {}
    d['version'] = '2'  # because we will be using the version 2 of the API
    # The rest of these are obtained from our environment. Don't forget
    # to do "source cloudclass-rc.sh"
    #
    d['username'] = "mukhopa"
    d['api_key'] = "ayan12345"
    d['auth_url'] = "https://keystone.isis.vanderbilt.edu:5000/v2.0"
    d['project_id'] = "Cloud Class"
    '''
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    '''
    # d['tenant_id'] = os.environ['OS_TENANT_ID']
    return d

def getFloatingIPByServerName(nova,serverName):
    servers = nova.servers.list()
    for server in servers:
        if server.name == serverName:
            try:
                return str(server.addresses["internal network"][1]["addr"])
            except IndexError:
                return None



# main
def setup (primary=True,counter=0):

    #set environment variables


    # get our credentials for version 2 of novaclient
    creds = get_nova_creds()

    # Now access the connection from which everything else is obtained.
    try:
        nova = client.Client (**creds)
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    #  creating a server needs the "create_server" function on the compute
    # object. To do that we must first create a key-value dictionary of
    # the server's attributes
    #
    # retrieve the underlying uuids (references) for various attributes
    imageref = nova.images.find (name="ubuntu-14.04")
    flavorref = nova.flavors.find (name="m1.small")
    sgref = nova.security_groups.find (name="default")
    # for some reason, this is not working.
    #netref = nova.networks.find (name="internal network")
    if primary:
        vmName = 'ayan-ubuntu-test-vm'
    else:
        vmName =  'ayan-ubuntu-test-vm' +str(counter)
    attrs = {
        'name' : vmName,
        'image' : imageref,
        'flavor' : flavorref,
        # providing the ref this way for security group is not working
        #'security_groups' : sgref,
        'key_name' : 'ayan_horizon',
        # I was going to do the following but does not work
        # 'nics' : [{'net-id' : netref.id}]
        'nics' : [{'net-id' : 'b16b0244-e1b5-4d36-90ff-83a0d87d8682'}]
        }

    try:
        serverName = vmName
        serverList = nova.servers.list()
        serverExists = False # to check if server already exists

        for counterServers in range(len(serverList)):
            #print str(serverList[counterServers]).split(":")[1].strip().split(">")[0]
            if serverName == str(serverList[counterServers]).split(":")[1].strip().split(">")[0]:
                serverExists = True
                server = serverList[counterServers]
                break
        if not serverExists:
            server = nova.servers.create(**attrs)

    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    # we need to check if server is up
    while (server.status != 'ACTIVE'):
        print "Not active yet; sleep for a while"
        time.sleep (2)
        # we need to retrieve the status of the server from
        # the restful API (it does not get updated dynamically in the
        # server object we have)
        server = nova.servers.find(name=serverName)

    if primary==True:
        #check if the created serve already has a floating ip or not
        ip = getFloatingIPByServerName(nova,serverName)
        print ip
        if ip==None:
            print "Adding floating IP"
            try:
                #check list of unassigned ips and add the first one
                #get list of floating ips and check unassigned
                floatingIPs = nova.floating_ips.list()
                for ip in floatingIPs:
                    if ip._info["instance_id"] == None:
                        server.add_floating_ip (address=ip._info["ip"])
                        break
            except:
                print "Exception thrown: ", sys.exc_info()[0]
                server.delete ()
                raise
     
# invoke main
# if __name__ == "__main__":
#     setup()#setup primary vm
#     setup(primary=False,counter=1)#setup secondary vm
#     secondaryVMCounter+=1



    
