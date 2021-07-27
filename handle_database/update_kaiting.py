import time
from pymysql import connect
import logging
from logging import info
logging.getLogger().setLevel(logging.INFO)
class Update():
    def __init__(self):
        self.con = connect(host='192.168.1.252', user='wanghu', password='wanghu123', db='company')
        # self.con = connect(host='localhost', user='root', password='123456', db='test')
        self.cursor = self.con.cursor()
        self.data = []
        self.de_count = 0
        self.up_count = 0

    #更新案件表中的所有相同的forid
    def update_maintable(self):
        sql = '''SELECT * FROM `stang_company_kaiting_anjian` WHERE forid in (SELECT forid FROM `stang_company_kaiting_anjian` GROUP BY forid HAVING COUNT(*)>1)'''
        info('正在查询中...')
        time.sleep(1)
        self.cursor.execute(sql)
        count = 0
        for item in self.cursor.fetchall():
            count += 1
            print('当前数据为:', item)
            id = item[0]
            forid = item[1]
            update_sql = '''UPDATE `stang_company_kaiting_anjian` SET forid={} WHERE id={}'''.format(id, id)
            info('开始执行更新操作...')
            self.cursor.execute(update_sql)
            info('操作成功')
        info('总共操作了%s条'%count)
        self.con.commit()
        self.cursor.close()
        self.con.close()

    def update_null_forid(self):
        sql = '''SELECT * FROM `stang_company_kaiting` as a LEFT JOIN `stang_company_kaiting_anjian` as b ON a.forid=b.forid WHERE b.forid is null'''
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        total = 0
        delet = 0
        updat = 0
        for r in result:
            total += 1
            dataid = r[0]
            caseNo = r[4]
            hdate = r[5]
            # 去查caseNo存在的那条数据
            sql = '''SELECT hearingDate,forid FROM `stang_company_kaiting_anjian` WHERE caseNo="{}"'''.format(caseNo)
            self.cursor.execute(sql)
            ret = self.cursor.fetchall()    #可能查出来多个结果
            if ret:
                flag = False
                for item in ret:
                    if item[0] == hdate:
                        flag = True
                        sql = '''UPDATE stang_company_kaiting SET forid={} WHERE id={}'''.format(item[1], dataid)
                        self.cursor.execute(sql)
                        info('更新了一条数据')
                        updat += 1
                        break
                if not flag:
                    info('删除了一条空数据')
                    self.delete_data(dataid)
                    delet += 1
            # forid为空，caseNo也没有
            else:
                self.delete_data(dataid)
                delet += 1
                info('删除了一条空数据')
        self.con.commit()
        print('总数据：', total)
        print('更新数据：', updat)
        print('删除数据：', delet)
        self.cursor.close()
        self.con.close()

    def delete_data(self, dataid):
        sql = '''DELETE FROM `stang_company_kaiting` WHERE id={}'''.format(dataid)
        self.cursor.execute(sql)

    def compare(self, data):
        cid = data[1]
        forid = data[2]
        caseNo = data[4]
        hearingDate = data[5]
        #第一次self.data是空
        if len(self.data) < 1:
            return 0
        if self.data[2] == forid and self.data[4] != caseNo:
            if self.data[1] == cid:
                return self.data[4]
            else:
                return 0
        else:
            return 0

    def update_data(self):
        sql = '''SELECT t.* FROM `stang_company_kaiting` AS t,(SELECT cid, forid FROM `stang_company_kaiting` GROUP BY cid,forid HAVING (COUNT(cid) > 1) AND (COUNT(forid) > 1)) AS a WHERE t.cid=a.cid AND t.forid=a.forid'''
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        info('查询成功！现在开始比较...')
        for i in result:
            ret = self.compare(i)
            if ret == 0:
                self.data = i
                continue
            else:
                forid = i[2]
                self.change(forid)
                self.data = i

    def change(self, forid):
        sql = '''SELECT * FROM `stang_company_kaiting` WHERE forid={}'''.format(forid)
        self.cursor.execute(sql)
        item = self.cursor.fetchall()
        # 需要更改的forid
        for i in item:
            data_id = i[0]
            forid = i[2]
            caseNo = i[4]
            hearingDate = i[5]
            anjian_sql = '''SELECT caseNo FROM `stang_company_kaiting_anjian` WHERE forid={}'''.format(forid)
            self.cursor.execute(anjian_sql)
            r = self.cursor.fetchall()
            if r[0][0] == caseNo:
                continue
            else:
                flag = False
                for incre in range(-1, 4):
                    update_sql = '''SELECT caseNo FROM `stang_company_kaiting_anjian` WHERE forid={}'''.format(forid+incre)
                    self.cursor.execute(update_sql)
                    t = self.cursor.fetchall()
                    try:
                        if t[0][0] == i[4]:
                            info('*'*20)
                            time.sleep(0.25)
                            info('id为%s修改之前的forid为%s'%(data_id, forid))
                            info('id为%s修改之后的forid为%s'%(data_id, forid+incre))
                            # print('假装更新')
                            self.update(forid+incre, data_id)
                            flag = True
                            break
                    except IndexError:
                        flag = False
                if not flag:
                    info('存在forid找不到的情况!')
                    status_code = self.update_by_caseNo(caseNo, hearingDate)
                    if status_code == 0:
                        info('forid及caseNo没有,删除当前记录！')
                        self.delete_data(data_id)
                        self.de_count += 1
                    else:
                        # print('处理后的假装更新')
                        self.update(status_code, data_id)

    def update_by_caseNo(self, caseNo, hearingDate):
        sql = '''SELECT * FROM `stang_company_kaiting_anjian` WHERE caseNo="{}"'''.format(caseNo)
        self.cursor.execute(sql)
        ret = self.cursor.fetchall()
        if len(ret) < 1:
            return 0
        else:
            # 更新为日期相同的那个forid
            for item in ret:
                if hearingDate == item[4]:
                    return item[1]
            return 0

    def update(self, forid, cid):
        self.up_count += 1
        update_sql = '''UPDATE stang_company_kaiting SET forid={} WHERE id={}'''.format(forid, cid)
        self.cursor.execute(update_sql)


if __name__ == "__main__":
    up = Update()
    up.update_data()
    up.con.commit()
    up.cursor.close()
    up.con.close()
    print('总共更新了%s条数据' % up.up_count)
    print('总共删除了%s条数据' % up.de_count)
    # up.update_null_forid()
    # up.update_maintable()