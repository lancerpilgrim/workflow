#!/bin/bash
#
#######
#
#
#   
PATH=/sbin:/bin:/usr/sbin:/usr/bin
SCRIPT_PATH=/web/script
LOG_PATH=/var/log/ab_monitor
LOG=/var/log/ab_monitor/portal.log

if [ ! -d $LOG_PATH ]; then
    mkdir $LOG_PATH
fi

DATE=`date -d "today" +"%Y-%m-%d %H:%M:%S"`
PORTAL=`ps -eF | grep "python" | grep "portal_server.py" | grep -v "grep" | wc -l`
RADIUS=`ps -eF | grep "python" | grep "radius_server.py" | grep -v "grep" | wc -l`
SPORTAL=`ps -eF | grep "python" | grep "portal.py" | grep -v "grep" | wc -l`
NGINX=`ps -eF | grep "nginx" | grep -v "grep" | wc -l`

if [ "$PORTAL" == "0" ]; then
    echo "$DATE Portal services have problem, restart" >> $LOG
    $SCRIPT_PATH/portal start
fi

if [ "$RADISU" == "0" ]; then
    echo "$DATE Radius services has problem, restart" >>$LOG
    $SCRIPT_PATH/radius start
fi

if [ "$SPORTAL" == "0" ]; then
    echo "$DATE White name list server has problem, restart" >>$LOG
    $SCRIPT_PATH/sportal start
fi
# crontab -e
# check service running every 5 minutes
# */5 * * * * bash monitor.sh
