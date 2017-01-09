#! /bin/bash

1. redirect
    like 
        ftp -i -n 192.168.21.46 <<EOF
        user zjk zjk123
        ls
        EOF 

2. pipe
    like
      echo 'password' | passwd -stdin username
      echo 'zjk123' | sudo -S cp file1 /etc/hosts

3. expect
    like
        set timeout 30
        spawn ssh -l jikuan.zjk 10.125.25.189
        expect "password:"
        send "zjk123\r"
        interact
