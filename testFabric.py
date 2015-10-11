from fabric.api import env, execute, task
import cuisine

env.hosts = "10.10.1.76"
env.user = "mukhopa"
env.password = "ayan12345"
env.key_filename = "ayan_horizon.pem"

@task
def update():
    sudo('apt-get update')

execute(update)