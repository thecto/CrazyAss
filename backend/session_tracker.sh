#!/bin/bash

md5_str=$1

for i in $(seq 1 30);do
    ssh_pid=$(ps -ef |grep $md5_str |grep -v grep |grep -v session_tracker.sh |grep -v sshpass |awk '{print $2}')
    echo "ssh session pid:"$ssh_pid
    if [ "$ssh_pid" = "" ];then
        sleep 1
        continue
    else
        today=$(date  "+%Y_%m_%d")
        today_audit_dir="logs/audit/$today"
        echo "today_audit_dir: $today_audit_dir"
        if [ -d $today_audit_dir ];then
            echo " ----start tracking log---- "
        else
            echo "dir not exist"
            echo "today dir: $today_audit_dir"
            sudo mkdir $today_audit_dir
        fi;
        # 给sudo传递密码
        echo 123456 | sudo -S /usr/bin/strace -ttt -f -p $ssh_pid -o "$today_audit_dir/$md5_str.log"
        break
    fi;
done;


# 如果在linux执行此shell脚本时报错"syntax error near unexpected token `$'do\r''"
# 解决方法：sudo sed -n 's/\r//' session_tracker.sh