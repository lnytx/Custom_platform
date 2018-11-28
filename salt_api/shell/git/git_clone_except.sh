#!/bin/bash
user=root
pwd=root
host=192.168.216.128
center_path=/soft/projects/EC_MY
dest_path=/opt/OMS
p_dest=`dirname $dest_path`
cd $p_dest
yum install -y expect
mkdir -p $dest_path
/usr/bin/expect << EOF
spawn git clone root@$host:$center_path
expect {
        -re "Permission denied, please try again." {
                send_user "Error:Permission denied.\n"
                exit
        }
                -re "Connection refused" {
                send_user "Error:Connection refused.\n"
                exit
        }
        timeout {
                exit
        }
        eof {
                exit
        }
        -re "Are you sure you want to continue connecting (yes/no)?" {
                send "yes\r"
                exp_continue
        }
        -re "assword:" {
                send "$pwd\r"
                exp_continue
        }
}
#interact
expect eof
EOF
