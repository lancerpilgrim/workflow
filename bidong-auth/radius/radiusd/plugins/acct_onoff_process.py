#!/usr/bin/env python
#coding=utf-8
from twisted.python import log
# from radiusd.store import store
from radiusd.settings import *
import account
import logging


def process(req=None,user=None,runstat=None,**kwargs):
    if  req.get_acct_status_type() not in (STATUS_TYPE_ACCT_ON,STATUS_TYPE_ACCT_OFF):
        return

    if req.get_acct_status_type() == STATUS_TYPE_ACCT_ON:
        account.unlock_online(req.get_nas_addr(),None,STATUS_TYPE_ACCT_ON)
        runstat.acct_on += 1  
        log.msg('bas accounting on success',level=logging.INFO)
    else:
        account.unlock_online(req.get_nas_addr(),None,STATUS_TYPE_ACCT_OFF)
        runstat.acct_off += 1  
        log.msg('bas accounting off success',level=logging.INFO)
