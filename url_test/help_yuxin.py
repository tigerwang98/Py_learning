# encoding: utf-8
"""
@project = Py_learing
@file = help_yuxin
@author= wanghu
@create_time = 2021/11/23 9:32
"""
import requests
from lxml import etree
import time
import sys
import redis

class Test():
    def __init__(self):
        self.redis_key = 'help_yuxin'
        self.rd = redis.Redis(host='localhost', password='', port=6379, db='0')
        self.header = {
            'Cookie': 'orgId=; configId=; homeConfigId=81b0c456-c6a8-4e25-9416-25f7cf5f6c06; studyProgress={"studyTime":{"0":185966,"1":34,"2":186000}}',
            'Authorization': 'Bearer__5ede1f89c0fc7e7df643e540a914f8ea',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        }
        # self.header = self.login
        self.exam_id = '13049e31-3220-490f-81a7-f29412875f27'
        self.answer = []
        self.update = False

    @property
    def login(self):
        account = 'sc140465'
        password = 'Yy998877'
        validate_code = ''

        return

    #根据redis题库给出答案
    def select_answer(self, question):
        if self.rd.hexists(self.redis_key, question):
            return self.rd.hget(self.redis_key, question)
        return

    # 根据做题记录的id更新redis题库
    def update_questions(self, param):
        url = 'https://mooc.ctt.cn/api/v1/exam/exam/front/score-detail?examRecordId=%s&_=%s' % (param, int(time.time()))
        res = requests.get(url=url, headers=self.header)
        if res:
            html = res.json()
            count = 0
            for question in html['paper']['questions']:
                daan = []
                count += 1
                title = question['content']
                answers = question['questionAttrCopys']
                # 判断题
                if question['type'] == 3:
                    if answers[0]['value'] == "1":
                        answer = '正确'
                    else:
                        answer = '错误'
                    self.rd.hset(self.redis_key, title,answer)
                else:
                    for answer in answers:
                        if answer['type'] == '0':
                            daan.append(answer['value'].strip().replace('\n', '').replace('\r', ''))
                        self.rd.hset(self.redis_key, title, ",".join(daan))

    # 获取本次考试的题目
    def get_exam_questions(self):
        url = 'https://mooc.ctt.cn/api/v1/exam/exam/front/exam-paper?clientType=1&examId=%s&_=%s' % (self.exam_id, int(time.time()))
        ret = requests.get(url=url, headers=self.header)
        if ret:
            count = 0
            exam_record_id = ret.json()['examRecord']['id']
            for question in ret.json()['paper']['questions']:
                count += 1
                print('当前已做到第%s题' % count)
                if not self.do_exam(question):
                    print('发现题库中没有此题！')
                    self.update = True
                    break
            self.submit_paper(exam_record_id)

    # 做本次考试的题
    def do_exam(self, question):
        daan = {}
        title = question['content']
        qid = question['id']
        option = dict()
        # 判断题
        if question['questionAttrCopys'][0]['type'] == '3':
            answer = self.select_answer(title)
            if not answer:
                return False
            # 判断题答案(变量名定义实在是麻烦)
            x = '1' if answer == '正确' else '0'
            daan = {
                "questionId": qid, "answer": x
            }
        else:
            for options in question['questionAttrCopys']:
                # 将返回的选项数据格式化存到option中
                option[options['value'].strip()] = options['name']
            answer = self.select_answer(title)
            if not answer:
                return False
            else:
                # 多选题
                if ',' in answer.decode():
                    j = []
                    for i in answer.decode().split(','):
                        j.append(str(option[i]))
                        daan = {
                            "questionId": qid, "answer": '%s' % ",".join(j)
                        }
                # 单选题
                else:
                    daan = {
                        "questionId": qid, "answer": '%s' % option[answer.decode()]
                    }
        self.answer.append(daan)
        return True

    # 获取每次做题记录的id
    def update_question_list(self):
        exam_record_list = []
        url = 'https://mooc.ctt.cn/api/v1/exam/exam-record/front/page?examId=13049e31-3220-490f-81a7-f29412875f27&page=1&pageSize=100&_=%s'% int(time.time())
        res = requests.get(url=url, headers=self.header)
        if res:
            for item in res.json()['items']:
                exam_record_list.append(item['id'])
        return exam_record_list

    # 交卷
    def submit_paper(self, exam_record_id):
        noAnswerCount = 60 - int(len(self.answer))
        url = 'https://mooc.ctt.cn/api/v1/exam/exam-record/front/submitPaper'
        header = {
            'Authorization': 'Bearer__5ede1f89c0fc7e7df643e540a914f8ea',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'homeConfigId=81b0c456-c6a8-4e25-9416-25f7cf5f6c06; orgId=; configId=; acw_tc=3ccdc14916376583920904294e1b36070e170f0a56cf3f60625a7d00306c52; studyProgress={"studyTime":{"0":185991,"1":34,"2":186025}}',
        }
        param = {
            'examId': self.exam_id,
            'examRecordId': exam_record_id,
            'submitType': 'Hand',
            'clientType': '1',
            'submitDetailType': '2',
            'clientVersion': 'Chrome/92.0.4515.131',
            'checkings': '[]',
            'noAnswerCount': noAnswerCount,
            'answeredCount': len(self.answer),
            'lastCacheTime': int(time.time()),
            'fullAnswerRecords': str(self.answer),
            'answerRecords': str(self.answer),
        }
        ret = requests.post(url=url, headers=header, data=param)
        if ret:
            if ret.json()['status'] == 1:
                print('提交成功!')
                if len(self.answer) > 59:
                    print('所有题都做完了!即将退出...')
                    sys.exit(0)
            else:
                print(ret.json()['msg'])
                raise Exception

if __name__ == '__main__':
    t = Test()
    count = 0
    while True:
        count += 1
        print('当前是第%s次做题,希望这次不用更新题库...' % count)
        questions = t.get_exam_questions()
        # 本次做题有题库中没有的,提交本次考试并更新题库
        if t.update:
            t.answer.clear()
            print('正在更新题库... ...')
            record_list = t.update_question_list()
            for record in record_list:
                t.update_questions(record)
            print('题库更新成功!')
            t.update = False