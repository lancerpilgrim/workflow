#!/bin/bash
#
# program: cut nginx log based on the date
# 
# author : hayate
#
log_path=/var/log/nginx
nginx_path=$log_path/old
pid_path=/var/run/nginx.pid

# make sure the nginx log path existed
if [ ! -e $nginx_path ]; then
    mkdir -p $nginx_path
fi

mv $log_path/access.log $nginx_path/access_$(date -d "yesterday" +"%Y-%m-%d").log
mv $log_path/error.log $nginx_path/error_$(date -d "yesterday" +"%Y-%m-%d").log

# send signal to nginx main process
kill -USR1 $(cat $pid_path)

# run crontab -e in root
# do each day at 0:00
# add 0 0 * * * bash $cut_nginx_logs.sh
