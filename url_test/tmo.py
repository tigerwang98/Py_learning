import copy
from copy import deepcopy

a = [1,2,[3,4]]
b = a.copy()
c = deepcopy(a)
print(b)
print(c)