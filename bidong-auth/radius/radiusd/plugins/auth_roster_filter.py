#!/usr/bin/env python
#coding=utf-8
from radiusd.plugins import error_auth
# from radiusd.store import store

def process(req=None,resp=None,user=None,**kwargs):
    """check block roster"""
    return resp

    # macaddr = req.get_mac_addr()
    # if store.is_black_roster(macaddr):
    #     return error_auth(resp,"user macaddr in blacklist")
    # return resp
