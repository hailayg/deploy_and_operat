#!/usr/bin/env python3
import os
from sys import argv
import time

# delete key
os.system("openstack keypair delete p-key")

# delete floating IP\
os.system('openstack floating ip list | grep "." | cut -d"|" -f"3">floating_ip')
os.system('grep -v "Floating" floating_ip > temphost && mv temphost floating_ip') 
os.system('grep -v "+--" floating_ip > temphost && mv temphost floating_ip')
with open("floating_ip")as f:
    for fp in f:
        pp=fp.rstrip()
        cmd='openstack floating ip delete {}'.format(pp)
        os.system(cmd)

# delete router
os.system("openstack router unset --external-gateway --tag p-tag p-router")
os.system("openstack router remove subnet p-router p-subnet")
os.system("openstack router delete p-router")

# port delete
os.system('openstack port list | grep "port" | cut -d"|" -f"3" >nodes')
with open("nodes") as f:
    for line in f:
        cmd = 'openstack port delete {}'.format(line)
        os.system(cmd)

# deleting nodes
os.system('openstack server list | grep "p-tag" | cut -d"|" -f"3" >nodes')
with open("nodes") as f:
    for line in f:
        cmd = 'openstack server delete {}'.format(line)
        os.system(cmd)
os.system('grep -v "10.0.1" hosts > temphost && mv temphost hosts')   
os.system('grep -v "ansible_ssh_common_args=" hosts > temphost && mv temphost hosts')

# delete subnet poop and subnet
os.system("openstack subnet  delete p-subnet")
os.system("openstack subnet pool delete p-pool")


# delete network
os.system("openstack network delete p-network")

# delete security group
os.system("openstack security group delete p-security")
