#!/bin/bash
user=root
pwd=root
dest_path=/soft/EC_MY
option='git --no-pager  log 1'
cd $dest_path
/usr/bin/expect << EOF
spawn $option
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
