config = {
    'debug':True,
    'tz':'CST-8',
    'secret':'Bidong_Wifi',
    'pid_path':'/siov/opt/bidong/run',
    'log_path':'/siov/opt/bidong/logs',
    'www_path':'/www/bidong/portal',

    'bidong' : 'http://mbd.cniotroot.cn/',

    'database':{
        'dbtype':'mysql',
        # 'host':'183.63.152.237',
        #'host':'14.23.62.180',
        # 'host':'172.16.36.11',
        'host':'172.16.17.32',
        'port':6006,
        'db':'bidong',
        'charset':'utf8',
        # 'user':'root',
        'user':'portal',
        'passwd':'7I48T1Se^@',
        # 'user':'bidong',
        # 'passwd':'Bd_123456',
        'maxusage':500,
        'read_timeout':10,
        'write_timeout':15,
    },

    'mongo_config':{
        #'uri':'mongodb://bidong:wifi_BD*@14.23.62.180:27517,14.23.62.181:27517/ap?replicaSet=bidong_nodes',
        'uri':'mongodb://siov:zlZ835@TaQ7I@172.16.36.13:27017/ap',
        'safe':True,
    },

    'KEY1':'4D59BF5CE76$JHUJ80B1*.3713BB6#5B',
    'KEY2':'D1.9BF5CE76$J*HJ80B1*.3K%NBB6#5B',

    'acctport':1813,
    'authport':1812,
    'adminport':1815,
    'cache_timeout':600,
    'logfile':'/siov/opt/bidong/logs/radiusd/radius.log',
    'auth_logfile':'/siov/opt/bidong/logs/radiusd/auth_radius.log',
    'acct_logfile':'/siov/opt/bidong/logs/radiusd/acct_radius.log',

    # 
    'reject_delay':3,
    
    'max_session_timeout':86400,   #max session time one day
    'expire_notify_days':7,         # notify before expire days

    'portal_config':{
        'max_bytes':4*1024*1024,
        'backup_count':2,
        'debug':1,
        'nas_port':2000,
        'nas_timeout':10,
        'secret':'BiDong_wifi09*76',
    },

    'weixin':{
        'appid':'wx3e09c0b3f5639426',
        'secret':'0b27f4decd12d953e673a88df03be427',
    },

    'logging_config':{
        'version':1,
        'formatters':{
            'detailed':{
                'class':'logging.Formatter',
                'format':'%(asctime)s -6d %(module) -16s %(levelname) -8s: %(message)s',
            },
            'warning':{
                'class':'logging.Formatter',
                'format':'%(asctime)s -6d %(module) -16s lineNo: %(lineno) -4d %(levelname) -8s: %(message)s',
            },
        },
        'root':{
            'level':'INFO',
            'handlers':['file', 'console']
        },
        'handlers':{
            'file':{
                'class':'logging.handlers.RotatingFileHandler',
                'filename':'portal',
                'mode':'a',
                'maxBytes':4*1024*1024,
                'backupCount':2,
                'level':'INFO',
                'formatter':'detailed',
            },
            'console':{
                'class':'logging.StreamHandler',
                'level':'DEBUG',
                'formatter':'detailed',
            },
        },
    },

    'RJ_AC' : {
        '172.29.1.246' : {'vendor':'ruijie', 'mask':1, 'pn':10002},
    },

    'SMS_GW' : {
        '',
    }
}

import sys
sys.modules[__name__] = config
