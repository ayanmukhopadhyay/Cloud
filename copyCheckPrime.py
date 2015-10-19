from fabric.api import env, execute, task
from fabric.operations import run, put

import sys

env.user = "ubuntu"
env.key_filename = "ayan_horizon.pem"
env.hosts = [sys.argv[1]]
env.reject_unknown_hosts = False

@task
def copy():
    put('/home/ubuntu/Cloud/checkPrime.py', '/home/ubuntu/')
    print "copied the file into " + env.hosts[0]

execute(copy)

