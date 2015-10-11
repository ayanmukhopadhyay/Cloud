from fabric.api import env, execute, task
import cuisine
from fabric.operations import sudo

env.hosts = "10.10.1.76"
env.user = "ubuntu"
#env.password = "ayan12345"
env.key_filename = "ayan_horizon.pem"

@task
def update():
    #sudo('rm /home/ubuntu/testFile.txt')
    sudo('ls')	
#execute(update)
