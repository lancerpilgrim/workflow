#!/bin/bash
#
###
# Portal service. {start, stop}
#
#
# 2015/03/31    hayate
set -e

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
CELERY=/bin/celery
# PYTHON=/usr/local/python-2.7.9/bin/python
# PYTHON=/usr/bin/python2.7
# LOG=/var/log/radiusd
TASK_PATH=/web/radius

LOG=/var/log/celery

USER=java

DESC=celery_task

# test -x $TWISTD || exit 1
test -x $CELERY || exit 1

# create necessary logs directory
if [ ! -d $LOG ]; then
    mkdir $LOG
fi
chown $USER:$USER $LOG

case "$1" in
    start)
        echo "Starting $DESC service: "
        cd $TASK_PATH
	echo 'sudo -u $USER $CELERY multi start portal --app=task --concurrency=500 \
            --pidfile=$LOG/%n.pid --logfile=$LOG/%n%I.log --loglevel=info -P eventlet
          '
        sudo -u $USER $CELERY multi start portal --app=task --concurrency=500 \
            --pidfile=$LOG/%n.pid --logfile=$LOG/%n%I.log --loglevel=info -P eventlet
#sudo -u java /bin/celery multi start portal --app=task --concurrency=500 --pidfile=/var/log/celery/%n.pid --logfile=/var/log/celery/%n%I.log --loglevel=info -P eventlet

        echo "$DESC."
        ;;
    stop)
        echo "Stop $DESC service: "
        # kill $(cat $TASK_PID) && rm -rf $TASK_PID
        $CELERY multi stop portal --pidfile=$LOG/portal.pid
        echo "$DESC stoped."
        ;;
    restart)
        echo "Restart $DESC server: "
        sudo -u $USER $CELERY multi restart portal --app=task \
            --pidfile=$LOG/portal.pid --logfile=$LOG/%n%I.log 
        echo "$DESC."
        ;;
    *)
        echo "Usage: $DESC {start|stop|restart}"
        exit 1
        ;;
esac
exit 0

