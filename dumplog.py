#!/usr/bin/env python
#-*- coding:utf8 -*-

import os
import time


log = './log/xtop.log'
F = open(log, 'a', encoding='utf8')

line = 'xbase-11:50:53.416-T27630:[Debug]-(xudp_socket.cc: SendDataWithProp:594): [metrics]{"category":"demo","tag":"bbb","type":"sometype","content":{"key1":"value1","key2":"value2"}}\n'

while True:
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.write(line)
    F.flush()
    time.sleep(0.1)

F.close()
