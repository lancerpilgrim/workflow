#!/usr/bin/env python
import logging

#coding=utf-8
# from DBUtils.PooledDB import PooledDB
from DBUtils.PersistentDB import PersistentDB
# from beaker.cache import CacheManager
# import functools
# import settings
import datetime
try:
    import MySQLdb
except:
    pass

# import string
__PASSWORD__ = ''.join(('abcdefghijkmnpqrstuvwxyz', 'ABCDEFGHJKLMNPQRSTUVWXYZ', '123456789', '~!@#$^&*<>=_'))

__cache_timeout__ = 600

# cache = CacheManager(cache_regions= {'short_term':{'type':'memory', 
#                                                    'expire':__cache_timeout__}})

ticket_fds = [
    'user', 'acct_input_octets', 'acct_output_octets', 'acct_input_packets', 'acct_output_packets', 
    'acct_session_id', 'acct_session_time', 'acct_start_time', 'acct_stop_time', 
    'acct_terminate_cause', 'frame_netmask', 'framed_ipaddr', 'is_deduct', 'nas_addr',
    'session_timeout', 'start_source', 'stop_source', 'mac_addr', 'ap_mac'
]

class Connect:
    def __init__(self, dbpool):
        self.conn = dbpool.connect()

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.conn.close()

class Cursor:
    def __init__(self, dbpool):
        self.conn = dbpool.connect()
        self.cursor = dbpool.cursor(self.conn)

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.conn.close()

class MySQLPool():
    def __init__(self, config):
        self.dbpool = PersistentDB(
            creator=MySQLdb,
            db=config['db'],
            host=config['host'],
            port=config['port'],
            user=config['user'],
            passwd=config['passwd'],
            charset=config['charset'],
            maxusage=config['maxusage'],
            # MySQLdb support, version > 1.2.5, mysql > 5.1.12
            read_timeout=config['read_timeout'],
            write_timeout=config['write_timeout'],
        )

    def cursor(self, conn):
        return conn.cursor(MySQLdb.cursors.DictCursor)

    def connect(self):
        return self.dbpool.connection()

pool_class = {'mysql':MySQLPool}

class Store():
    def setup(self, db_config):
        self.dbpool = MySQLPool(db_config)
        # global __cache_timeout__
        # __cache_timeout__ = config['cache_timeout']

    def _combine_query_kwargs(self, **kwargs):
        '''
            convert query kwargs to str
        '''
        query_list = []
        for key, value in kwargs.iteritems():
            if isinstance(value, int):
                query_list.append('{}={}'.format(key, value))
            else:
                query_list.append('{}="{}"'.format(key, value))

        return ' and '.join(query_list) 

    def deal_pn_user_history(self, pn):
        '''
        '''
        with Connect(self.dbpool) as conn:
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            start,num=0,200
            while True:
                sql = '''select bd_account.* from bd_account 
                right join pn_{pn} on bd_account.mobile=pn_{pn}.mobile 
                order by bd_account.user
                '''.format(pn=pn)
                # where bd_account.mobile order by bd_account.user limit {start},{num}
                # '''.format(pn=pn, start=start, num=num)

                print(sql)

                cur.execute(sql)

                results = cur.fetchall()
                print('{}: {}'.format(len(results), sql))
                for item in results:
                    if item['ends'] < 10 and item['user']:
                        sql = 'update bd_account set ends=2 where user="{}"'.format(item['user'])
                        print(sql)
                        cur.execute(sql)
                    # delete user's history records
                    # sql = 'delete from mac_history where user="{}"'.format(item['user'])
                    cur.execute(sql)

                conn.commit()
                start += len(results)

                # if len(results) < num:
                #     break

            print('count: {}'.format(start))
                # if len(results) < num:
                #     print('count: {}'.format(start))
                #     start += len(results)
                #     break
                # start += num

                

    def clear_ac_online_records(self, acs):
        '''
        '''
        with Connect(self.dbpool) as conn:
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            if not acs:
                return
            acs = ','.join(['"{}"'.format(ac) for ac in acs])
            sql = 'delete from online where nas_addr in ({})'.format(acs)
            cur.execute(sql)

            conn.commit()


db = Store()
