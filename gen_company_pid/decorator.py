# _*_ coding:utf-8 _*_
import time


def checkConnect(func):
    def inner(self, *args, **kwargs):
        _number, _status = 0, True
        while _status and _number <= 5:
            try:
                self.conn.ping()
                _status = False
            except:
                time.sleep(1)
                self.conn = self.__conn_252()
                if self.conn:
                    self.cursor = self.conn.cursor()
                    _status = False
                _number += 1
        return func(self, *args, **kwargs)
    return inner
