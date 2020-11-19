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
    # @param conf p2p module config
    #
    # @return
    @classmethod
    def run(cls, payload, qmap, conf):
        slog.debug("P2pModule run begin")

        priority = 2
        status = cls.package_alarm(payload, qmap, conf, priority)

        slog.debug("P2pModule run end")
        return status
