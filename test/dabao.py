# https://cuiqingcai.com/
from redis import StrictRedis, ConnectionPool

pool = ConnectionPool(host='localhost', port=6379, password='', db=0)
r = StrictRedis(connection_pool=pool)
r.set('name', 'Bob')
print(r.get('name'))