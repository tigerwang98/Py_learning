# encoding: utf-8
"""
@project = Py_learing
@file = twisted_test
@author= wanghu
@create_time = 2021/8/5 15:21
"""
from twisted.internet import protocol,reactor

class Echo(protocol.Protocol):
    def dataReceived(self, data: bytes):
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

reactor.listenTCP(8000, EchoFactory())
reactor.run()