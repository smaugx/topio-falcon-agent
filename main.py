#!/usr/bin/env python
#-*- coding:utf8 -*-

import time
import os
import json
from multiprocessing import Process, Queue, Lock, Manager

# log eater
from logger.log_eater import LogEater

# metrics filter, get metrics log which will be putted to remote
from logger.metrics_filter  import MetricsFilter

# every kind of modules
from logger.base_module import BaseModule
from logger.demo_module import DemoModule
from logger.p2p_module import P2pModule

# report alarm to remote
from reporter.report_alarm import ReportAlarm 

import common.config as config
from common.slogging import slog


#######global var#########

# store log line from (tail -f)
LogQueue = Queue(config.QMAXSIZE)

# store alarm data(readonly, use in multiprocess)
AlarmQueueMap = {
        0: Queue(config.QMAXSIZE),
        1: Queue(config.QMAXSIZE),
        2: Queue(config.QMAXSIZE),
        }

# register module here(readonly, use in multiprocess)
ModuleMap = {
        'demo'        : DemoModule.run,
        'p2p'         : P2pModule.run,
        'default'     : BaseModule.run,
        }


####### func begin ########


# log eater: eat the last log line and store in log queue
def run_logeater():
    global LogQueue

    # list of path
    log_path = config.LogEaterConfig.get('log_path')
    if not log_path:
        slog.error("empty log_path, eat log failed")
        return

    logeater = LogEater(LogQueue, log_path)

    # will block here
    logeater.run()


def run_loganalyzer(shared_local_info):
    global LogQueue, AlarmQueueMap, ModuleFunc

    while True:
        log_line = ''
        try:
            # block here, wait log line ready
            log_line = LogQueue.get(block = True)
        except Exception as e:
            slog.warn("catch exception:{0} when get from log queue".format(e))
            continue

        payload =  MetricsFilter.run(log_line)
        if not payload:
            continue

        category = payload.get('category')
        ModuleFunc = ModuleMap.get(category)
        if not ModuleFunc:
            #slog.error("category:{0} not support, filter failed".format(category))
            #continue
            ModuleFunc = ModuleMap.get('default')

        conf = config.AnalyzeConfig.get(category)
        ModuleFunc(payload, AlarmQueueMap, conf, shared_local_info)

def run_logreporter():
    global AlarmQueueMap
    report_conf = config.ReportConfig
    alarm_reporter = ReportAlarm(AlarmQueueMap, report_conf)
    # will block here if no data
    alarm_reporter.run()


if __name__ == '__main__':
    shm_path = '/dev/shm/topio-falcon-shared'
    with Manager() as MG:
        # shared dict with other process
        shared_local_info = MG.dict()

        sh_dict = {}
        if os.path.exists(shm_path):
            try:
                sh_dict = json.loads(open(shm_path, 'r').read())
                print("load local shared info from {0}:".format(shm_path))
                print(json.dumps(sh_dict, indent=4))
            except Exception as e:
                pass

        shared_local_info['tnode'] = sh_dict.get('tnode')
        shared_local_info['ip'] = sh_dict.get('ip')

        # create log eater process
        pg_logeater = Process(target=run_logeater, args=())


        # create log analyzer process
        pg_loganalyzers = []
        an_worker = config.AnalyzeConfig.get('worker')
        for i in range(an_worker):
            pg_loganalyzers.append(Process(target = run_loganalyzer, args=(shared_local_info,)))

        # create log reporter process
        pg_logreporters = []
        re_worker = config.ReportConfig.get('worker')
        for j in range(re_worker):
            pg_logreporters.append(Process(target = run_logreporter, args = ()))


        # start all process
        print("start log eater worker")
        pg_logeater.start()

        print("start log analyze worker")
        for p in pg_loganalyzers:
            p.start()

        print("start log reporter worker")
        for p in pg_logreporters:
            p.start()

        while True:
            time.sleep(60)
            with open("/dev/shm/topio-falcon-shared", 'w', encoding = 'utf-8') as fout:
                sh_dict = {}
                for k,v in shared_local_info.items():
                    sh_dict[k] = v
                fout.write(json.dumps(sh_dict))
