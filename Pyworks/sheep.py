#!/bin/env python 
#encoding=utf-8
 
import time
import os
import sys
import pexpect
# regular expression
import re 
from threading import Thread
from optparse import OptionParser
from multiprocessing import Process

def Usage():
    print '-i|--ipc=xx.xx.xx'  
    print '-s|--startip=50'
    print '-e|--endip=149'
        
def add_trust(cmd):
    ssh=pexpect.spawn(cmd)
#    ssh.logfile = sys.stdout
    try:
#        index=ssh.expect(['.*\]#','\(yes/no\)\?','password:'],timeout=20)
        index=ssh.expect(['.*\]#','\(yes/no\)\?','password:'])
        if index == 0 :
            ssh.sendline('echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAIEA+qA1cYcQ6+Rwy/SZniThxSZ/t/qCZ2ivtO3b8WeQOo2XWVs/OEjSqFtkikC+dZSLYYMCXQozKWPQPmIIdDyhVk1Zt/0WlfxQ2nsb/qwXJUaBGpG9QEuQkqz3dVma2cfSK0RU2az4wmNCChbp1cWScUos8Lm/iIj107NJHiP+sdM= work@db-jomo-jcm01.db01.baidu.com" >/root/.ssh/authorized_keys')
            ssh.expect(['.*\]#'])
            ssh.sendline('echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAzpPnH9eku7HpHV7ge2QfXU8DHE+GAOBLQ8zvhAzrjci0yV8dd0xNRyT/ySBwem5jQFjVw8KGoGu2p+/jIPN1DdWvbFd5ZnFIZ/VwqKasJLNgi37nCkaYjrmINjYjwm1M6F6nN2ymp5JZ+nyOK+YyshcCqr0/iPCEICJSz6LSKSmc3w+YQv9gFBwuiwvUxm4vU6VcRmXW7AhdxQnGjDK54r5kMENXnG9W9BkfyRaNorrIFY7sRa8uBZUmVO7kVLp+hy1ZV5NYefwfsqpHFrQIi1i80DqS7oEW8GESshmV3gvqLzbBvFnWFEBwbI/y7N7YltWCAV82aQRWdi045c2f7w== root@tc-sys-cdn-oc01.tc.baidu.com" >>/root/.ssh/authorized_keys')
            ssh.expect(['.*\]#'])
            ssh.sendline('chown root.root /root/.ssh/authorized_keys && chmod 644 /root/.ssh/authorized_keys && echo \'78g*tw23d!sq@CDN\' | passwd root --stdin')
            ssh.expect(['.*\]#'])
            ssh.close()
        if index == 1 :
            ssh.sendline('yes')
            ssh.expect(['password:'])
            ssh.sendline('IN*it2016@cdn')
            ssh.expect(['.*\]#'])   
            ssh.sendline('echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAIEA+qA1cYcQ6+Rwy/SZniThxSZ/t/qCZ2ivtO3b8WeQOo2XWVs/OEjSqFtkikC+dZSLYYMCXQozKWPQPmIIdDyhVk1Zt/0WlfxQ2nsb/qwXJUaBGpG9QEuQkqz3dVma2cfSK0RU2az4wmNCChbp1cWScUos8Lm/iIj107NJHiP+sdM= work@db-jomo-jcm01.db01.baidu.com" >/root/.ssh/authorized_keys')
            ssh.expect(['.*\]#'])
            ssh.sendline('echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAzpPnH9eku7HpHV7ge2QfXU8DHE+GAOBLQ8zvhAzrjci0yV8dd0xNRyT/ySBwem5jQFjVw8KGoGu2p+/jIPN1DdWvbFd5ZnFIZ/VwqKasJLNgi37nCkaYjrmINjYjwm1M6F6nN2ymp5JZ+nyOK+YyshcCqr0/iPCEICJSz6LSKSmc3w+YQv9gFBwuiwvUxm4vU6VcRmXW7AhdxQnGjDK54r5kMENXnG9W9BkfyRaNorrIFY7sRa8uBZUmVO7kVLp+hy1ZV5NYefwfsqpHFrQIi1i80DqS7oEW8GESshmV3gvqLzbBvFnWFEBwbI/y7N7YltWCAV82aQRWdi045c2f7w== root@tc-sys-cdn-oc01.tc.baidu.com" >>/root/.ssh/authorized_keys')
            ssh.expect(['.*\]#'])
            #ssh.sendline('chown root.root /root/.ssh/authorized_keys && chmod 644 /root/.ssh/authorized_keys')
            ssh.sendline('chown root.root /root/.ssh/authorized_keys && chmod 644 /root/.ssh/authorized_keys && echo \'78g*tw23d!sq@CDN\' | passwd root --stdin')
            ssh.expect(['.*\]#'])
            ssh.close()
        if index == 2 :
            ssh.sendline('IN*it2016@cdn')
            ssh.expect(['.*\]#'])
            ssh.sendline('echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAIEA+qA1cYcQ6+Rwy/SZniThxSZ/t/qCZ2ivtO3b8WeQOo2XWVs/OEjSqFtkikC+dZSLYYMCXQozKWPQPmIIdDyhVk1Zt/0WlfxQ2nsb/qwXJUaBGpG9QEuQkqz3dVma2cfSK0RU2az4wmNCChbp1cWScUos8Lm/iIj107NJHiP+sdM= work@db-jomo-jcm01.db01.baidu.com" >/root/.ssh/authorized_keys')
            ssh.expect(['.*\]#'])
            ssh.sendline('echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAzpPnH9eku7HpHV7ge2QfXU8DHE+GAOBLQ8zvhAzrjci0yV8dd0xNRyT/ySBwem5jQFjVw8KGoGu2p+/jIPN1DdWvbFd5ZnFIZ/VwqKasJLNgi37nCkaYjrmINjYjwm1M6F6nN2ymp5JZ+nyOK+YyshcCqr0/iPCEICJSz6LSKSmc3w+YQv9gFBwuiwvUxm4vU6VcRmXW7AhdxQnGjDK54r5kMENXnG9W9BkfyRaNorrIFY7sRa8uBZUmVO7kVLp+hy1ZV5NYefwfsqpHFrQIi1i80DqS7oEW8GESshmV3gvqLzbBvFnWFEBwbI/y7N7YltWCAV82aQRWdi045c2f7w== root@tc-sys-cdn-oc01.tc.baidu.com" >>/root/.ssh/authorized_keys')
            ssh.expect(['.*\]#'])
            #ssh.sendline('chown root.root /root/.ssh/authorized_keys && chmod 644 /root/.ssh/authorized_keys')
            ssh.sendline('chown root.root /root/.ssh/authorized_keys && chmod 644 /root/.ssh/authorized_keys && echo \'78g*tw23d!sq@CDN\' | passwd root --stdin')
            ssh.expect(['.*\]#'])
            ssh.close()
    except :
        ssh.close()
        sys.exit(10)

def connect_host(ipc,startip,endip):
    processes=[]
    error_list=[]
    for ipd in range(int(startip),int(endip)+1): 
        cmd='ssh root@' + ipc + '.' + '%s'%ipd 
        p=Process(target=add_trust,name=ipd,args=(cmd,))
        p.start()
        processes.append(p)
    for i in processes:
        i.join()
#        print i.exitcode
#        print i.pid
        if i.exitcode ==0:
            print '\033[1;32;40m Add '+ipc+'.'+str(i.name)+' ok\033[1;37;40m'
        else:
            print '\033[1;31;40m Add '+ipc+'.'+str(i.name)+'  error\033[1;37;40m'
            error_list.append(i.name)
    print '\033[1;31;40m All error host '+str(error_list)+' \033[1;37;40m'

def main():
    usage = '''
    Usage:
    ./add_trust_root.py -i 12.13.44 -s 50 -e 149
    '''
    parser=OptionParser()
    parser.add_option('-i','--ipc',action='store',type='string',dest='ipc',help='please input ipc,like 213.22.55')
    parser.add_option('-s','--startip',action='store',type='int',dest='startip',help='start ipd,like 50')
    parser.add_option('-e','--endip',action='store',type='int',dest='endip',help='end ipd,like 149')
    (opt,args)=parser.parse_args()
    if opt.startip>=255 or opt.endip>=255 or opt.startip<0 or opt.endip<0:
        print '\033[1;31;40mstartip or endip is error must >0 and <255\033[1;37;40m'
        print usage
        sys.exit(1)
    if opt.startip>opt.endip:
        print '\033[1;31;40mstartip cat not greater endip\033[1;37;40m'
        print usage
        sys.exit(1)
    pat=re.compile('((25[0-4])|(2[0-4]\\d)|(1\\d\\d)|([1-9]\\d)|[1-9])(\\.((25[0-4])|(2[0-4]\\d)|(1\\d\\d)|([1-9]\\d)|[1-9])){2}')  
    if not pat.match(opt.ipc):
        print '\033[1;31;40mipc is error\033[1;37;40m'
        print usage
        sys.exit(1)
    connect_host(opt.ipc,opt.startip,opt.endip)   
        
if __name__=='__main__':
    main()

