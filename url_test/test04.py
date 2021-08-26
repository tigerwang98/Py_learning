# encoding= utf-8
"""
@project = temp
@file = test04
@author= wanghu
@create_time = 2021/6/24 19=15
"""
# import random
# print("%s %s 6-22 * * *" % (random.randint(1, 60), random.randint(1, 60)))
import json,re
from dateparser import parse
from urllib.parse import quote
import copy

a = [1,2,3, [4,5]]

c = copy.copy(a)
d = copy.deepcopy(a)

a[-1][0] = 10
print(a)
print(c)
print(d)

