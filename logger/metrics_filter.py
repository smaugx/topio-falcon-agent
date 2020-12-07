#!/usr/bin/env python
#-*- coding:utf8 -*-

import os
import uuid
import json

from common.slogging import slog

# debug:   xbase-11:50:53.416-T27630:[Debug]-(xudp_socket.cc: SendDataWithProp:594): [metrics]{"category":"aaa","tag":"bbb","type":"sometype","content":{"key1":"value1","key2":"value2"}}
# release: xnetwork-02:16:51.450-T32679:[Keyfo]-(): [metrics]{"category":"aaa","tag":"bbb","type":"sometype","content":{"key1":"value1","key2":"value2"}}

class MetricsFilter(object):
    def __init__(self):
        return

    # @param line log line
    #
    # @return payload json metrics object 
    @classmethod
    def run(cls, line):
        slog.debug("line:{0}".format(line))

        payload = None
        try:
            if line[-1] == '\n':
                line = line[:-1]

            line = line.decode('utf8')
            if line.find("metrics") == -1:
                return None

            sp_line = line.split('[metrics]')
            if not sp_line or len(sp_line) != 2:
                slog.warn("found invalid metrics line:{0}".format(line))
                return None

            try:
                payload = json.loads(sp_line[1])
            except Exception as e:
                slog.warn("invalid json line:{0}, load failed".format(line))
                return None

            if not payload.get('category'):
                slog.warn("invalid json line:{0}, get field category failed".format(line))
                return None
        except Exception as e:
            slog.warn("catch exception:{0} line:{1}".format(e, line))
            return None
        
        # finally get payload we want
        #{
        #    "category": "aaa",
        #    "content": {
        #        "key2": "value2",
        #        "key1": "value1"
        #    },
        #    "tag": "bbb",
        #    "type": "sometype"
        #}
        return payload
