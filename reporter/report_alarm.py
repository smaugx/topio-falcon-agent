#!/usr/bin/env python
#-*- coding:utf8 -*-

import time
import json
import uuid
import requests
import hashlib

from common.slogging import slog

class ReportAlarm(object):
    # @param qmap map of queue with priority
    # @param conf config of reporter
    # 
    # @return
    def __init__(self, qmap, conf):
        self.conf_ = conf
        self.qmap_ = qmap
        self.F = open("./log/alarm.data", 'a', encoding='utf8')

    # will block here
    def run(self):
        # rename
        return self.get_alarmq_with_priority()


    def get_alarmq(self, q):
        alarm_payload = None
        try:
            # will not block, if empty raise Empty exception
            alarm_payload = q.get(block = False) 
        except Exception as e:
            pass
        return alarm_payload

    # will block here
    def get_alarmq_with_priority(self):
        if not self.qmap_:
            return None
        keys = self.qmap_.keys()
        keys = list(keys)
        # from high priority to low priority; from 0 to 2; keys is [0,1,2]
        keys.sort()

        while True:
            for priority in keys:
                q = self.qmap_.get(priority)
                while True:
                    alarm_payload = self.get_alarmq(q)
                    if not alarm_payload:
                        break

                    # post to remote
                    self.report_remote(alarm_payload)

            time.sleep(0.2)


    def report_remote(self, alarm_payload):
        '''
        # alarm_payload example:
        {
            "priority":2,
            "alarmid":"288c0c2c-414a-4ba1-90ac-750a7883d2ac",
            "tnode":"xxxxxxxxxxx@127.0.0.1:9000",
            "timestamp":1605855035,
            "payload":{
                "category":"p2p",
                "tag":"kad_info",
                "type":"real_time",
                "content":{
                    "local_nodeid":"000000010000ffffffffffffffffffff000000004e63488d763c618ed9d63aba49c11586",
                    "service_type":9223090561894842368,
                    "xnetwork_id":0,
                    "zone_id":1,
                    "cluster_id":0,
                    "group_id":0,
                    "neighbours":13,
                    "public_ip":"127.0.0.1",
                    "public_port":9003
                }
            }
        }
        '''

        url = self.conf_.get('url')
        if not url:
            return False

        payload = {
                'topic': 'ANALYSE',
                'msg': '',
                'sign': ''
                }

        '''
        msg = {
                'data': [
                    {
                        'category': 'topnetwork',
                        'properties': alarm_payload,
                    },
                    ]
                }
        '''

        msg = {
                "userid":1,
                "appVersion":"",
                "country":"",
                "sign":"",
                "netType":"",
                "bid":"",
                "idfa":"",
                "osVersion":"",
                "osType":1,
                "appName":"",
                "deviceid":"",
                "sessionid":"",
                "ip":"",
                "sourceSystem":"",
                "data": [
                    {
                        "properties": alarm_payload,
                        "event":"topnetwork", # ??
                        "category":"topnetwork",
                        "time": alarm_payload.get('timestamp')
                    }
                ]
        }



        self.F.write('{0}\n'.format(json.dumps(msg)))
        slog.debug(json.dumps(msg, indent=4))
        msg_str  = json.dumps(msg)
        payload['msg'] = msg_str
        digest = ''
        if len(msg_str) < 128:
            digest = hashlib.sha256(msg_str).hexdigest()
        else:
            m = msg_str[:64] + msg_str[-64:]
            digest = hashlib.sha256(m.encode('utf8')).hexdigest()

        payload['sign'] = digest
        slog.debug(json.dumps(payload, indent=4))

        try:
            r = requests.post(url, data = json.dumps(payload))
            if r.status_code == 200:
                slog.debug('post ok')
            slog.debug(r.text)
        except Exception as e:
            slog.warn("catch Exception:{0}".format(e))
            return True
