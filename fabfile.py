from fabric.api import env, execute, task
from fabric.operations import sudo, run, put

env.hosts = "10.10.1.195"
env.user = "ubuntu"
env.key_filename = "ayan_horizon.pem"

@task
def ls():
    #sudo('rm /home/ubuntu/testFile.txt')
    #local('ls')
    ret = run('ls')
    print "returned: " + ret

@task
def copy():
    ret = put('/home/ubuntu/testFabric', '/home/ubuntu/')

@task
def ls_root():
    ret = run('ls /')
    print "returned: " + ret

execute(ls)
#print "retrun value"
#print retVal
execute(copy)
execute(ls)
#execute(ls_root)

