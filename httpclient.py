#!/bin/python
#
# sample http client
#

# @Amogh: test comment

import sys
import httplib
from datetime import datetime

def main ():
    print "Instantiating a connection obj"
    try:
        conn = httplib.HTTPConnection ("localhost", "8080")
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    print "sending a GET request to our http server"
    try:
        timePre = datetime.now()
        conn.request("GET", "?53-isNumberPrime")
        timePost = datetime.now()
        latency = (timePost - timePre).total_seconds()
        print latency
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    print "retrieving a response from http server"
    try:
        resp = conn.getresponse ()
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    print "printing response headers"
    try:
        for hdr in resp.getheaders ():
            print hdr
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

    print "printing data"
    try:
        data = resp.read ()
        print "Length of data = ", len(data)
        print data
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise

# invoke main
if __name__ == "__main__":
    sys.exit (main ())
    
