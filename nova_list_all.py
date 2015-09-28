#!/usr/bin/env python
import os
import sys
from novaclient.v2 import client

# Institution: Vanderbilt University
# Code created for the CS4287-5287 course
# Author: Aniruddha Gokhale
# Created: Fall 2015

# See http://docs.openstack.org/developer/python-novaclient/ for Python
# binding to nova reference
#
# see example at http://docs.openstack.org/user-guide/sdk_compute_apis.html

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
    d['tenant_id'] = os.environ['OS_TENANT_ID']
    return d

def main ():
    
    # get our credentials for version 2 of novaclient
    creds = get_nova_creds()

    # Now access the connection from which everything else is obtained.
    try:
        nova = client.Client (**creds)
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise
        
    # let's print the availability zones
    print "----------------------------------------------------------"
    print "All the availability zones"
    try:
        for zone in nova.availability_zones.list():
            print zone
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
         
    # let's print the hosts
    print "----------------------------------------------------------"
    print "All the hosts"
    try:
        for host in nova.hosts.list():
            print host
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
         
    # let's print the suported flavors
    print "----------------------------------------------------------"
    print "All the flavors"
    try:
        for flavor in nova.flavors.list():
            print flavor
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
         
    # let's print the available images
    print "----------------------------------------------------------"
    print "All the images"
    try:
        for image in nova.images.list():
            print image
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
         
    # Let's print the available networks
    print "----------------------------------------------------------"
    print "All the networks"
    try:
        for network in nova.networks.list():
            print network
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
         
    # let's print the currently active servers
    print "----------------------------------------------------------"
    print "All the servers"
    try:
        for server in nova.servers.list():
            print server
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
         
    # let's print the floating IP pools
    print "----------------------------------------------------------"
    print "All the floating IP address pools"
    try:
        for fipp in nova.floating_ip_pools.list():
            print fipp
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
         
    # let's print the floating IPs
    print "----------------------------------------------------------"
    print "All the floating IP addresses"
    try:
        for fip in nova.floating_ips.list():
            print fip
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
         
    # let's print the keypairs
    print "----------------------------------------------------------"
    print "All the keypairs"
    try:
        for kp in nova.keypairs.list():
            print kp
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
         
    # let's print the security groups
    print "----------------------------------------------------------"
    print "All the security groups"
    try:
        for sg in nova.security_groups.list():
            print sg
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
         
    # let's print the services
    print "----------------------------------------------------------"
    print "All the services"
    try:
        for svc in nova.services.list():
            print svc
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        pass
         
# invoke main
if __name__ == "__main__":
    sys.exit (main ())
    
