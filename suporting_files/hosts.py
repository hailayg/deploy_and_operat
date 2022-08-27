#!/usr/bin/env python3
import os
import time
count=0
cmd='openstack server list | grep "p-tag-HAproxy" | cut -d"|" -f"5" | cut -d"=" -f"2" | cut -d"," -f"1">temp_ip'
os.system(cmd)
with open("temp_ip", 'r') as f:
    ip=f.read()
haproxy="p-tag-HAproxy ansible_host="+str(ip)
with open("hosts", 'r+') as f:
    ll=f.readlines()
    if haproxy not in ll:
        ll.insert(1,haproxy)
        f.seek(0)
        f.writelines(ll)
cmd1='openstack server list | grep "p-tag-node" | cut -d"|" -f"5" | cut -d"=" -f"2">temp_ip'
os.system(cmd1)
with open("temp_ip", 'r') as f:
    k=1
    for lin in f:
        with open("hosts", 'r+') as b:
            for line in b:
                if lin in line:
                    count+=1
        if count==0:
            li=lin.rstrip()
            cm='openstack server list | grep {} | cut -d"|" -f"3" >nodes'.format(li)
            os.system(cm)
            with open("nodes", 'r') as d:
                ip=d.read()
            ip=ip.rstrip()
            ip1=ip+" ansible_host="+str(lin)
            with open("hosts", 'r+') as b:
                l1=b.readlines()
                ll.insert(k+2,ip1)
                b.seek(0)
                b.writelines(ll)
        k+=1
cmd2='openstack server list | grep "p-tag-bastion" | cut -d"|" -f"3 5" | cut -d"=" -f"2" | cut -d"," -f"2">temp_ip'
os.system(cmd2)
with open("temp_ip", 'r') as f:
    ip2=f.read()
    ip2=ip2.rstrip('\n')
    ip2=ip2.lstrip()
cmd3="ansible_ssh_common_args="+"\'-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ProxyCommand="+"\" ssh -W %h:%p -q ubuntu@"+ip2+"-i pub-key\"\'"+"\n"
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
