# encoding: utf-8
"""
@project = Py_learing
@file = kafka_test
@author= wanghu
@create_time = 2021/8/4 10:35
"""
import json
import time

from kafka import KafkaProducer,KafkaConsumer
from multiprocessing import Process

def productor():
    print('This is process 1')
    producer = KafkaProducer()
    msg_dict = {
    'sleep_time': 1,
    'db_config': {
        'database': 'test',
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        },
        'table': 'msg',
        'msg': 'This is a test kafka demo',
    }
    msg = json.dumps(msg_dict)
    producer.send('test', msg.encode('utf-8'), partition=0)
    # producer.close()

def consum():
    print('This is process 2')
    time.sleep(3)
    consumer = KafkaConsumer('test')
    for msg in consumer:
        recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
        print(recv)

if __name__ == '__main__':
    c = Process(target=consum, args=())
    c.start()
    for i in range(10):
        p = Process(target=productor, args=())
        p.start()