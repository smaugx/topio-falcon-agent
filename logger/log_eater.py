#!/usr/bin/env python
#-*- coding:utf8 -*-


import subprocess
import select

from common.slogging import slog

class LogEater(object):
    # @param log_queue tail -f log, get the last line and store in queue
    # @param log_path_list  list of log path
    #
    # @return
    def __init__(self, log_queue, log_path_list):
        self.log_queue_ = log_queue
        self.log_path_list_  = log_path_list

    def put_alarmq(self, data):
        try:
            self.log_queue_.put(data, block=True, timeout =2)
        except Exception as e:
            return False
        return True


    # will block here
    def run(self):
        if not self.log_queue_:
            slog.error("log_queue invalid, eat log failed")
            return

        p = select.poll()
        sf_list = []
        for log_path in self.log_path_list_:
            slog.info("eat log:{0}".format(log_path))
            sf = subprocess.Popen(['tail','-F',log_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.register(sf.stdout.fileno(), select.POLLIN)
            sf_list.append(sf)
        
        while True:
            # timeout is 1 ms; if timeout is none, will block here if no event
            for fd, event in p.poll(1):
                if not (event & select.POLLIN):
                    continue

                for sf in sf_list:
                    if fd == sf.stdout.fileno():
                        line = sf.stdout.readline()
                        if not line:
                            continue
                        if line[-1] == '\n':
                            line = line[:-1]
                        slog.debug("put log line:{0} to log queue, size:{1}".format(line, self.log_queue_.qsize()))
                        status = self.put_alarmq(line)
                        if not status:
                            slog.warn("put log line to log queue failed")
                        break
