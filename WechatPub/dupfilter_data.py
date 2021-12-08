# encoding: utf-8
"""
@project = Py_learing
@file = bloom_filter
@author= wanghu
@create_time = 2021/10/26 14:34
"""
import os
import platform
import cmath
from hashlib import md5
from redis import Redis
import logging
import BitVector
logging.basicConfig(level=logging.DEBUG)

class SimpleHash():  # 这里使用了bkdrhash的哈希算法
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret  # 控制哈系函数的值域

class BloomFilter(object,):
    def __init__(self, filename):
        '''
        :param filename: 去重文件名.
        这里是过滤将近 1E 个item所配置的过滤器(布隆过滤器大小计算器: http://www.ab173.com/convert/filesize.php)
        '''
        # <<表示二进制向左移动位数，比如2<<2, 2的二进制表示000010，向左移2位，就是001000，就是十进制的8
        self.bit_size = 2 << 26
        self.container_size = (-1) * self. bit_size * cmath.log(0.001) / (cmath.log(2) * cmath.log(2))  # 计算最佳空间大小
        self.container_size = int(self.container_size.real)  # 取整
        self.container = BitVector.BitVector(size=self.container_size)  # 分配内存
        self.seeds = [3, 5, 7, 11, 13, 31, 37, 61, 67, 101, 107, 151, 157]  # k=13
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))
        self.bloomfile = self.CreateBloomFile(filename)
        self.bloomfile_to_Memory(self.bloomfile)

    #生成重文件函数
    def CreateBloomFile(self, filename):
        filepath = ''
        if 'Windows' in platform.system():
            filepath = 'c:/new_BloomFile/'
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            f = open(filepath + filename+'.txt', 'a')
            f.close()
        elif 'Linux' in platform.system():
            filepath = '/home/hadoop/Youkexin/new_BloomFile/'
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            f = open(filepath + filename+'.txt', 'a')
            f.close()
        return filepath+filename+'.txt'

    #bloom文件超出限制处理函数
    def bloom_del(self, bloomfile, lines):
        new_lines = lines[5200000:]  # 只保留剩下大约160M的数据
        with open(bloomfile, 'a+')as fw:
            fw.seek(0)
            fw.truncate() #清空所有数据再写入
            for new_line in new_lines:
                fw.write(new_line)
        print('新的文件写入结束！')
        return new_lines

    #将布隆文件数据读取到内存
    def bloomfile_to_Memory(self, bloomfile):
        with open(bloomfile, 'r')as f:
            lines = f.readlines()
        filesize = os.path.getsize(bloomfile)
        if filesize == 0:
            return
        elif filesize/1024/1024 >= 240:
            print('文件大小为：%s,已经超过bloom文件限制240M,删除最早数据！' % (filesize/1024/1024))
            new_lines = self.bloom_del(bloomfile, lines)
        else:
            new_lines = lines
        for line in new_lines:
            loc = int(line.strip('\n'))
            try:
                self.container[loc] = 1
            except:
                print('blomm读取出错！', loc)

    #判断数据是否存在
    def exists(self, value):
        '''存在返回真，否则返回假'''
        if value == None:
            return False
        m5 = md5()
        m5.update(value.encode())
        value = m5.hexdigest()
        for func in self.hashfunc:
            loc = func.hash(str(value)) #内存位
            if self.container[loc] == 0:
                return False
        return True

    #向去重文件写入数据
    def mark_value(self, value):
        '''value是要标记的元素'''
        f = open(self.bloomfile, 'a')
        m5 = md5()
        m5.update(value.encode())
        value = m5.hexdigest()
        for func in self.hashfunc:
            loc = func.hash(str(value)) #内存位
            self.container[loc] = 1
            f.write(str(loc)+'\n')
        f.close()
        return

class RedisFilter():
    def __init__(self, key_name):
        self.redis_conn = Redis(host='192.168.1.196', password='', db='7', port=6379)
        self.key_name = key_name

    #判断数据是否存在
    def check_value(self, item):
        if self.redis_conn.sismember(self.key_name, item):
            return True
        else:
            return False

    #向去重文件写入数据
    def mark_value(self, value):
         self.redis_conn.sadd(self.key_name, value)

# 自定义异常
class SelectFilterError(Exception):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'Filter Error!Please Use \'Bloom\' or \'Redis\''

'''
* filter_method: 去重的方法
* filter_name: 去重的文件名或集合名
* url: 去重的链接
* dont_filter: 本次调用是否去重
'''
def filter_data(filter_method, filter_name, url, dont_filter=False):
    if dont_filter:
        logging.info('请注意!现在处于不去重状态')
        return False
    if filter_method == 'Bloom':
        bf = BloomFilter(filter_name)
        if bf.exists(url):
            logging.debug('Filtered offisite %s' % url)
            return False
        else:
            bf.mark_value(url)
            return True
    elif filter_method == 'Redis':
        rd = RedisFilter(filter_name)
        if rd.check_value(url):
            logging.debug('Filtered offisite %s' % url)
            return False
        else:
            rd.mark_value(url)
            return True
    else:
        raise SelectFilterError

if __name__ == '__main__':
    url = 'http://mp.weixin.qq.com/s?src=11&timestamp=1635242736&ver=3398&signature=SOIyFSz2JfzlCY2nZUvpsogZI1XpEW9N3G*MzflWV5-FMCY17pAhud7tWmTC3TRsCMANa8zsNIqdiMmFhiRKL8r-*rHykdgsH13dYOWU2j*dFg3klz7mg5CvhIou9kBj&new=1'
    rd = RedisFilter('WechatPub')
    if rd.check_value(url):
        logging.debug('Filted offisite %s' % url)
        print('有了')
    else:
        rd.mark_value(url)
        print('没有')