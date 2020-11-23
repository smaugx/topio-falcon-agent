#!/usr/bin/env python
#-*- coding:utf8 -*-


import subprocess
import select

from common.slogging import slog

class LogEater(object):
    # @param log_queue tail -f log, get the last line and store in queue
    # @param log_path  log path
    #
    # @return
    def __init__(self, log_queue, log_path):
        self.log_queue_ = log_queue
        self.log_path_  = log_path

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

        slog.info("eat log:{0}".format(self.log_path_))
        f = subprocess.Popen(['tail','-F',self.log_path_], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = select.poll()
        p.register(f.stdout)
        
        while True:
            if p.poll(1):
                line = f.stdout.readline()
                if not line:
                    continue
                if line[-1] == '\n':
                    line = line[:-1]
                slog.debug("put log line:{0} to log queue, size:{1}".format(line, self.log_queue_.qsize()))
                status = self.put_alarmq(line)
                if not status:
                    slog.warn("put log line to log queue failed")
