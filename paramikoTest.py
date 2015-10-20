from __future__ import print_function
from fabric.api import run, sudo, local, env
import paramiko
import socket

host1 = '129.59.107.170'
offline_host2 = '192.168.200.199'
host3 = '192.168.200.183'

env.hosts = [host1, offline_host2, host3]

def df_h():
    if _is_host_up(env.host, int(env.port)) is True:
        run("df -h | grep sda1")


def _is_host_up(host, port):
    # Set the timeout
    original_timeout = socket.getdefaulttimeout()
    new_timeout = 3
    socket.setdefaulttimeout(new_timeout)
    host_status = False
    try:
        transport = paramiko.Transport((host, port))
        host_status = True
    except:
        print('***Warning*** Host {host} on port {port} is down.'.format(
            host=host, port=port)
        )
    socket.setdefaulttimeout(original_timeout)
    return host_status

_is_host_up(host1,22)