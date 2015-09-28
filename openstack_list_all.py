#!/usr/bin/env python
import os
import sys
from openstack import connection
from openstack import profile

# Institution: Vanderbilt University
# Code created for the CS4287-5287 course
# Author: Aniruddha Gokhale
# Created: Fall 2015

# This uses the openstack sdk API
# See: http://python-openstacksdk.readthedocs.org/en/latest/users/index.html#api-documentation
# So far less success getting this to work compared to the project-specific 
# APIs.

# get our credentials from the environment variables
def get_openstack_creds():
    d = {}
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_name'] = os.environ['OS_TENANT_NAME']
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    return d

def main ():
    
    # get our credentials
    creds = get_openstack_creds()

    # Now access the connection from which everything else is obtained.
    try:
        conn = connection.Connection (**creds)
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    # hereon, we access the compute object of the connection and
    # list all the properties of the connection object

    # the flavors () is a generator function. So iterating thru it will
    # give us the next entry on its own
    print "----------------------------------------------------------"
    print "All the flavors with their details"
    try:
        for f in conn.compute.flavors ():
            print "**************************"
            print f
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
    
    # the images () is a generator function. So iterating thru it will
    # give us the next entry on its own
    print "------------------------------------------------------------------"
    print "All the images with their details"
    try:
        for img in conn.compute.images ():
            print "**************************"
            print img
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
    
    # the servers () is a generator function. So iterating thru it will
    # give us the next entry on its own
    print "------------------------------------------------------------------"
    print "All the server with less details"
    try:
        for srv in conn.compute.servers (details=True):
            print "**************************"
            print srv
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
    
    # the keypairs () is a generator function. So iterating thru it will
    # give us the next entry on its own
    print "------------------------------------------------------------------"
    print "All the keypairs with their details"
    try:
        for kp in conn.compute.keypairs ():
            print "**************************"
            print kp
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
    
    # the networks () is a generator function. So iterating thru it will
    # give us the next entry on its own
    print "------------------------------------------------------------------"
    print "All the networks with their details"
    try:
        for nw in conn.network.networks ():
            print "**************************"
            print nw
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
    
# invoke main
if __name__ == "__main__":
    sys.exit (main ())
    
