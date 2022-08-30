#!/usr/bin/env python3
import os
import time
import os.path
#variables
key='p-key'
net='p-network'
subpool='p-pool'
sub='p-subnet'
router='p-router'
port='p-port'
secgroup='p-security'
proxy='p-tag-HAproxy'
bastion='p-tag-bastion'
node='p-tag-node'
fl='1C-1GB-20GB'

#key 
ex=os.path.exists("files")
if ex==False:
    os.system('mkdir files')
os.system('openstack keypair list>files/nodes')
with open("files/nodes") as f:
    if key not in f.read():
        cmd='openstack keypair create {}> files/pub-key'.format(key)
        os.system(cmd)
        os.system('chmod 600 files/pub-key')

#Network
os.system('openstack network list>files/nodes')
with open("files/nodes") as f:
    if net not in f.read():
        cmd='openstack network create --tag p-tag {} -f json'.format(net)
        os.system(cmd)
#subnet pool
os.system('openstack subnet pool list>files/nodes')
with open("files/nodes") as f:
    if subpool not in f.read():
        cmd='openstack subnet pool create --pool-prefix 10.0.1.0/24 --tag p-tag {} '.format(subpool)
        os.system(cmd)

#subnet
os.system('openstack subnet list>files/nodes')
with open("files/nodes") as f:
    if sub not in f.read():
        cmd='openstack subnet create --subnet-pool {} --prefix-length 27 --dhcp --gateway 10.0.1.1 --ip-version 4 --network {} --tag p-tag {} '.format(subpool,net,sub)
        os.system(cmd)

#router
os.system('openstack router list>files/nodes')
with open("files/nodes") as f:
    if router not in f.read():
        cmd='openstack router create --tag p-tag {} '.format(router)
        os.system(cmd)
        cm='openstack router add subnet {} {}'.format(router,sub)
        os.system(cm)
        cm1='openstack router set --external-gateway ext-net {}'.format(router)
        os.system(cm1)

#port
    i=1
    while i<=3:
        os.system('openstack port list>files/nodes')
        with open("files/nodes") as f:
            por=port+str(i)
            if por not in f.read():
                cmd='openstack port create --network {} --tag p-tag {} '.format(net,por)
                os.system(cmd)
        i+=1

#router add properties


#security group
os.system('openstack security group list>files/nodes')
with open("files/nodes") as f:
    if secgroup not in f.read():
        cmd='openstack security group create --tag p-tag {}'.format(secgroup)
        os.system(cmd)
        os.system('openstack security group rule create --remote-ip 0.0.0.0/0 --dst-port 22 --protocol tcp --ingress p-security')
        os.system('openstack security group rule create --remote-ip 0.0.0.0/0 --dst-port 80 --protocol tcp --ingress p-security')
        os.system('openstack security group rule create --remote-ip 0.0.0.0/0 --dst-port 5000 --protocol tcp --ingress p-security')
        os.system('openstack security group rule create --remote-ip 0.0.0.0/0 --dst-port 6000 --protocol udp --ingress p-security')
        os.system('openstack security group rule create --remote-ip 0.0.0.0/0 --dst-port 53 --protocol udp --ingress p-security')
        os.system('openstack security group rule create --remote-ip 0.0.0.0/0 --dst-port 80 --protocol icmp --ingress p-security')

#nodes
os.system('openstack server list>files/nodes')
with open("files/nodes") as f:
    if proxy not in f.read():
        cmd='openstack server create --image "Ubuntu 20.04 Focal Fossa 20210616" --flavor {} --key-name {} --network {} --security-group {} {}'.format(fl,key,net,secgroup,proxy)
        os.system(cmd)
        os.system("openstack floating ip create ext-net -f json | jq -r '.floating_ip_address' > files/floating_ip")
        with open("files/floating_ip") as b:
            fip1=b.read()
        c='openstack server add floating ip {} {}'.format(proxy,fip1)
        os.system(c)
with open("files/nodes") as f:
    if bastion not in f.read():
        cmd1='openstack server create --image "Ubuntu 20.04 Focal Fossa 20210616" --flavor {} --key-name {} --network {} --security-group {} {}'.format(fl,key,net,secgroup,bastion)
        os.system(cmd1)
        os.system("openstack floating ip create ext-net -f json | jq -r '.floating_ip_address' > files/floating_ip")
        with open("files/floating_ip") as f:
            fip2=f.read()
        cc='openstack server add floating ip {} {}'.format(bastion,fip2)
        os.system(cc)
k=1
while k<=3:
    os.system('openstack server list>files/nodes')
    with open("files/nodes") as f:
        nod=node+str(k)
        if nod not in f.read():
            cmd2='openstack server create --image "Ubuntu 20.04 Focal Fossa 20210616" --flavor {} --key-name {} --network {} --security-group {} {}'.format(fl,key,net,secgroup,nod)
            os.system(cmd2)
    k+=1

#configuration
count=0
cmd='openstack server list | grep "p-tag-HAproxy" | cut -d"|" -f"5" | cut -d"=" -f"2" | cut -d"," -f"1">files/nodes'
os.system(cmd)
with open("files/nodes", 'r') as f:
    ip=f.read()
haproxy="p-tag-HAproxy ansible_host="+str(ip)
with open("hosts", 'r+') as f:
    ll=f.readlines()
    if haproxy not in ll:
        ll.insert(1,haproxy)
        f.seek(0)
        f.writelines(ll)
cmd1='openstack server list | grep "p-tag-node" | cut -d"|" -f"5" | cut -d"=" -f"2">files/nodes'
os.system(cmd1)
with open("files/nodes", 'r') as f:
    k=1
    for lin in f:
        with open("hosts", 'r+') as b:
            for line in b:
                if lin in line:
                    count+=1
        if count==0:
            li=lin.rstrip()
            cm='openstack server list | grep {} | cut -d"|" -f"3" >files/nodes'.format(li)
            os.system(cm)
            with open("files/nodes", 'r') as d:
                ip=d.read()
            ip=ip.rstrip()
            ip1=ip+" ansible_host="+str(lin)
            with open("hosts", 'r+') as b:
                l1=b.readlines()
                ll.insert(k+2,ip1)
                b.seek(0)
                b.writelines(ll)
        k+=1
cmd2='openstack server list | grep "p-tag-bastion" | cut -d"|" -f"3 5" | cut -d"=" -f"2" | cut -d"," -f"2">files/nodes'
os.system(cmd2)
with open("files/nodes", 'r') as f:
    ip2=f.read()
    ip2=ip2.rstrip('\n')
    ip2=ip2.lstrip()
cmd3="ansible_ssh_common_args="+"\'-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ProxyCommand="+"\" ssh -W %h:%p -q ubuntu@"+ip2+"-i files/pub-key\"\'"+"\n"
c=0
with open("hosts", 'r+') as b:
    for line in b:
        if cmd3 in line:
            c+=1
if c==0:
    with open("hosts", 'r+') as b:
        l1=b.readlines()
        ll.insert(11,cmd3)
        b.seek(0)
        b.writelines(ll)
