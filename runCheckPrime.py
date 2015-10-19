from fabric.api import env, execute, task
from fabric.operations import run, put

import sys

env.user = "ubuntu"
env.key_filename = "ayan_horizon.pem"
env.hosts = [sys.argv[1]]

@task
def runme():
    returnValue = run('python /home/ubuntu/checkPrime.py ' + sys.argv[2])
    # print "ran the file into " + env.hosts[0]
    print returnValue

execute(runme)


