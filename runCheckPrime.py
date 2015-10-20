from fabric.api import env, execute, task
from fabric.operations import run, put
import time

import sys

env.user = "ubuntu"
env.key_filename = "ayan_horizon.pem"
env.hosts = [sys.argv[1]]
env.reject_unknown_hosts = False

@task
def runme():
    counter = int(sys.argv[3])
    returnValue = run('python /home/ubuntu/checkPrime.py ' + sys.argv[2])
    # print "ran the file into " + env.hosts[0]
    if counter == 10:
        time.sleep(10)
    print "@"+str(returnValue)+"@"

execute(runme)


