#!/usr/bin/env python
#-*- coding:utf8 -*-

import queue

from logger.metrics_filter  import MetricsFilter
from logger.demo_module import DemoModule
from logger.p2p_module import P2pModule
from logger.contract_module import ContractModule
from reporter.report_alarm import ReportAlarm 

import common.config as config
from common.slogging import slog



QueueMap = {
        0: queue.Queue(config.QMAXSIZE),
        1: queue.Queue(config.QMAXSIZE),
        2: queue.Queue(config.QMAXSIZE),
        }

# register module here
ModuleMap = {
        'demo': DemoModule.run,
        'p2p': P2pModule.run,
        'contract': ContractModule.run,
        }

local_info_conf = config.LocalInfo

line_debug = 'xbase-11:50:53.416-T27630:[Debug]-(xudp_socket.cc: SendDataWithProp:594): [metrics]{"category":"demo","tag":"bbb","type":"sometype","content":{"key1":"value1","key2":"value2"}}'

line_release = 'xnetwork-02:16:51.450-T32679:[Keyfo]-(): [metrics]{"category":"demo","tag":"bbb","type":"sometype","content":{"key1":"value1","key2":"value2"}}'

p2p_config = config.P2pConfig
p2p_config['local_info'] = local_info_conf

payload =  MetricsFilter.run(line_debug)
category = payload.get('category')

ModuleFunc = ModuleMap.get(category)
if ModuleFunc:
    ModuleFunc(payload, QueueMap, p2p_config)
else:
    slog.error("category:{0} not support, filter failed".format(category))

report_conf = config.ReportConfig
alarm_reporter = ReportAlarm(QueueMap, report_conf)
alarm_reporter.run()
