#!/usr/bin/env python
#-*- coding:utf8 -*-

import os
import time
import uuid
import json

from common.slogging import slog

from logger.base_module import BaseModule

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

class P2pModule(BaseModule):
    def __init__(self):
        return

    # @param line log line
    # @param qmap  map of queue with priority
    # @param shared_info  shared info between all process
    # @param conf p2p module config
    #
    # @return
    @classmethod
    def run(cls, payload, qmap, conf, shared_info):
        slog.debug("P2pModule run begin")

        if not shared_info.get('tnode'):
            if payload.get('tag') and payload.get('tag') == 'kad_info':
                if payload.get('content') and payload.get('content').get('local_nodeid'):
                    if payload.get('content').get('local_nodeid').startswith("ffffff"):
                        root_id = payload.get('content').get('local_nodeid')
                        public_ip = payload.get('content').get('public_ip')
                        public_port = payload.get('content').get('public_port')
                        tnode = '{0}@{1}:{2}'.format(root_id, public_ip, public_port)
                        shared_info['tnode'] = tnode
                        shared_info['ip'] = public_ip
                        slog.warn("set tnode:{0}".format(tnode))

        priority = 2
        status = cls.package_alarm(payload, qmap, conf, shared_info, priority)

        slog.debug("P2pModule run end")
        return status
