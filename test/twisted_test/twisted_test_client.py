# encoding: utf-8
"""
@project = Py_learing
@file = twisted_test_client
@author= wanghu
@create_time = 2021/8/27 14:34
"""
from twisted.internet import reactor,protocol

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(b'Hello! World!')

    def dataReceived(self, data):
        print('Server said:', data)
        self.transport.loseConnection()

    def connectionLost(self, reason):
        print('connection lost')

class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()

    def clientConnectionFailed(self, connector, reason):
        print('connection failed - goodbye!')
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print('connection lost - goodbye!')
        reactor.stop()

reactor.connectTCP('localhost', 8000, EchoFactory())
reactor.run()