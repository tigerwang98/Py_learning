# encoding: utf-8
"""
@project = Py_learing
@file = kafka_test
@author= wanghu
@create_time = 2021/8/4 10:35
"""
import json
from kafka import KafkaProducer,KafkaConsumer
import multiprocessing

producer = KafkaProducer()
consumer = KafkaConsumer()

msg_dict = {
    'sleep_time': 10,
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
producer.send()