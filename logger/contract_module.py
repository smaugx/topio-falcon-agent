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
#            "category": "demo",
#            "content": {
#                "key2": "value2",
#                "key1": "value1"
#            },
#            "tag": "gossip",
#            "type": "runtime"
#        }
#}
#

class ContractModule(BaseModule):
    def __init__(self):
        return

    # @param line log line
    # @param qmap  map of queue with priority
    # @param conf module config
    #
    # @return
    @classmethod
    def run(cls, payload, qmap, conf = None):
        slog.debug("ContractModule run begin")

        priority = 2
        status = cls.package_alarm(payload, qmap, conf, priority)

        slog.debug("ContractModule run end")
        return status
