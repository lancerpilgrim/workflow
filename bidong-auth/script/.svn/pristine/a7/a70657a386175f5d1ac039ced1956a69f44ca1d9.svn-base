#!/bin/bash
#
###
# backup bidong
#
#
# 2015/009/30    hayate
set -e

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
# PYTHON=/usr/local/python-2.7.9/bin/python

mysqldump -uroot -pwifi_bd* bidong --lock-all-tables > /home/niot/wifi/db_back/bd_$(date "+%Y-%m-%d").sql

# run crontab -e in root
# do every sunday in 4 
# add 0 4 * * 0 bash dump_db.sh

