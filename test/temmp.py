import time
from threading import Thread
class Test:
    def __init__(self, param):
        self.param = param

    def __new__(cls, *args, **kwargs):
        if not hasattr(Test, '_instance'):
            Test._instance = object.__new__(cls)
        else:
            print('当前已经有一个这样的类了!')
        return Test._instance

    def __str__(self):
        return self.param

def task1():
    time.sleep(2)
    t = Test('haha')
    print(t.__repr__())
    print(t)

def task2():
    time.sleep(1)
    t = Test('xixi')
    print(t.__repr__())
    print(t)

for i in range(10):
    if i < 5:
        th = Thread(target=task1)
    else:
        th = Thread(target=task2)
    th.start()