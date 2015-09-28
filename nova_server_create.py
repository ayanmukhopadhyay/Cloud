#!/usr/bin/env python
import os
import sys
import time
from novaclient.v2 import client

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
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    # d['tenant_id'] = os.environ['OS_TENANT_ID']
    return d

# main
def main ():
    
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
    
    attrs = {
        'name' : 'asg-ubuntu-test-vm',
        'image' : imageref,
        'flavor' : flavorref,
        # providing the ref this way for security group is not working
        #'security_groups' : sgref,
        'key_name' : 'gokhale_horizonisis',
        # I was going to do the following but does not work
        # 'nics' : [{'net-id' : netref.id}]
        'nics' : [{'net-id' : 'b16b0244-e1b5-4d36-90ff-83a0d87d8682'}]
        }

    try:
        server = nova.servers.create (**attrs)
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
        server = nova.servers.find (name='asg-ubuntu-test-vm')
    
    # you should cycle through the floating ips and choose the one that is not
    # taken by someone yet. For now we are hardcoding it

    print "Adding floating IP"
    try:
        server.add_floating_ip (address="129.59.107.96")
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        server.delete ()
        raise
     
# invoke main
if __name__ == "__main__":
    sys.exit (main ())
    
