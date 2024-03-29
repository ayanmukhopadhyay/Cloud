#!/bin/python
#
# sample http client
#

# @Amogh: test comment

import sys
import httplib
from datetime import datetime
import random

def main ():
    print "Instantiating a connection obj"
    try:
        conn = httplib.HTTPConnection ("10.10.1.74", "8080")
    except:
        print "Exception thrown: ", sys.exc_info()[0]
        raise
    for counter in range(100):
        print "sending a GET request to our http server"
        try:
	    numberCheck = str(random.randint(1,5))
            timePre = datetime.now()
	    
            conn.request("GET", "?"+numberCheck+"-isNumberPrime")
            # conn.request("GET", "/testurl", str(53))
        except:
            print "Exception thrown: ", sys.exc_info()[0]
            raise

        print "retrieving a response from http server"
        try:
            resp = conn.getresponse ()
            #timePost = datetime.now()
            #latency = (timePost - timePre).total_seconds()
            #print latency
        except:
            print "Exception thrown: ", sys.exc_info()[0]
            raise
        #try:
            #print "sending latency report back to server"
            #conn.request("GET","?"+str(latency)+"-latencyReport")
            #resp = conn.getresponse ()
        #except:
            #print "Exception thrown: ", sys.exc_info()[0]
            #raise

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

    conn.request("GET", "?"+str(-1)+"-over")
    resp = conn.getresponse ()

# invoke main
if __name__ == "__main__":
    sys.exit (main ())
    
