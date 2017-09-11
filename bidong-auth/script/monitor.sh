#!/bin/bash
#
#######
#
#
#   
PATH=/sbin:/bin:/usr/sbin:/usr/bin
SCRIPT_PATH=/web/script
LOG=/var/log/ab_monitor/services.log

DATE=`date -d "today" +"%Y-%m-%d %H:%M:%S"`
BIDONG=`ps -eF | grep "python" | grep "main.py" | grep -v "grep" | wc -l`
CMS=`ps -eF | grep "python" | grep "cms.py" | grep -v "grep" | wc -l`
IMS=`ps -eF | grep "python" | grep "ims.py" | grep -v "grep" | wc -l`
NGINX=`ps -eF | grep "nginx" | grep -v "grep" | wc -l`

if [ "$BIDONG" == "0" ]; then
    echo "$DATE BIDONG services have problem, restart" >> $LOG
    $SCRIPT_PATH/bidong start
fi

if [ "$CMS" == "0" ]; then
    echo "$DATE CMS services has problem, restart" >>$LOG
    $SCRIPT_PATH/cms start
fi

# if [ "$IMS" == "0" ]; then
#     echo "$DATE IMS services has problem, restart" >>$LOG
#     $SCRIPT_PATH/ims start
# fi

# crontab -e
# check service running every 5 minutes
# */5 * * * * bash monitor.sh
