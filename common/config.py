#-*- coding:utf8 -*-

LOGLEVEL = 'debug'
LOGPATH = './log/falcon.log'

QMAXSIZE = 10000


AnalyzeConfig = {
        'worker': 2,
        'p2p': {
            'global_sample_rate': 1000,  # sample_rate%。
            'alarm_pack_num': 2,   # upload alarm size one time
            'config_update_time': 5 * 60,  # 5 min
            'grep_broadcast': {
                'start': 'true',
                'sample_rate': 200,    # 20%
                'alarm_type': 'packet',
                'network_focus_on': ['000000010000','000000020000', '0000000f0101', '0000000e0101', '0000000001'], # src or dest: rec;zec;edg;arc;aud/val
                'network_ignore':   [],  # src or dest
            },
            'grep_point2point': {
                'start': 'false',
                'sample_rate': 5,    # 1%
                'alarm_type': 'packet',
                'network_focus_on': ['000000010000','000000020000', '0000000f0101', '0000000e0101', '0000000001'], # src or dest: rec;zec;edg;arc;aud/val
                'network_ignore':   [],  # src or dest
            },
            'grep_networksize': {
                'start': 'true',
                'sample_rate': 50,  # 5%
                'alarm_type': 'networksize',
            },
            'system_cron': {
                'start': 'true',
                'alarm_type': 'system',
            },
            'system_cron': {
                'start': 'true',
                'alarm_type': 'system',
            }
        },
        'contract': {},
        'sync': {},
        'db': {},
} # end AnalyzeConfig


ReportConfig = {
        'worker': 2,
        #'url': 'http://apigateway.dt-dn1.com:9230/report/log/async',
        'url': 'http://gatewaylogv2.top123.info:9230/report/log/async',
        }

LogEaterConfig = {
        'log_path': [
            '/chain/log/xtop.log',
            '/root/topnetwork/log/xtop.log',
            '/home/topuser/topnetwork/log/xtop.log',
            '/tmp/rec1/xtop.log',
            ]
        }
