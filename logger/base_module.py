#!/usr/bin/env python
#-*- coding:utf8 -*-

import os
import time
import uuid
import json

from common.slogging import slog

#{
#        'priority':  priority,
#        'alarmid' :  '{0}'.format(uuid.uuid4()),
#        'tnode'   :  tnode,
#        'timestamp': int(time.time()),
#        'payload' :  {
#            "category": "p2p",
#            "content": {
#                "key2": "value2",
#                "key1": "value1"
#            },
#            "tag": "gossip",
#            "type": "runtime"
#        }
#}
#

class BaseModule(object):
    def __init__(self):
        return

    # @param line log line
    # @param qmap  map of queue with priority
    # @param shared_info  shared info between all process
    # @param conf module config
    #
    # @return
    @classmethod
    def run(cls, payload, qmap, conf, shared_info):
        slog.debug("BaseModule run begin")

        priority = 2
        status = cls.package_alarm(payload, qmap, conf, shared_info, priority)

        slog.debug("BaseModule run end")
        return status
    
    @classmethod
    def put_alarmq(cls, data, q):
        try:
            q.put(data, block=True, timeout =2)
        except Exception as e:
            return False
        return True

    @classmethod
    def package_alarm(cls, payload, qmap, conf, shared_info, priority = 2):
        tnode =  shared_info.get('tnode')
        if not tnode:
            slog.warn("tnode empty, not ready for alarm")
            # TODO(smaug)
            shared_info['tnode'] = 'xxxxxxxxxxx@127.0.0.1:9000'
            return False
        if not qmap.get(priority):
            slog.error("priority:{0} not support".format(priority))
            return False

        alarm_data = {
                'priority':  priority,
                'alarmid' :  '{0}'.format(uuid.uuid4()),
                'tnode'   :  tnode,
                'timestamp': int(time.time()),
                'payload' :  payload
                }

        # put original json object(not string) to queue
        if cls.put_alarmq(alarm_data, qmap.get(priority)):
            slog.debug("put data:{0} to alarm_queue_{1} size:{2} success".format(json.dumps(alarm_data), priority, qmap.get(priority).qsize()))
        else:
            slog.warn("put data:{0} to alarm_queue_{1} fail, error: full".format(json.dumps(alarm_data), priority))
        return True
