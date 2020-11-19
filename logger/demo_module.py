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

class DemoModule(BaseModule):
    def __init__(self):
        return
