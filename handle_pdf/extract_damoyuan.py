import re
info_str = '''4:165
5:基于坐标法的防风型整体钢腕臂预配工法
6:中国铁建电气化局集团有限公司
7:李继亮、秦俊非、连进、张桂平、李双双
8:166
9:重载电气化铁路隧道区承导线更换施工工法
10:中国铁建电气化局集团有限公司
11:李怀念、马昊博、郭航宇、杜乾友、单锋
12:167
13:客运专线隧道内信号轨旁设备支架式安装工法
14:中国铁建电气化局集团有限公司
15:杨帆、郭小波、杨阿龙、刘春平、赵瑞皎
16:168
17:信号电缆引入间组装支架电缆敷设施工工法
18:中国铁建电气化局集团有限公司
19:杨帆、张旭柏、关磊、任小涛、杨阿龙
20:169
21:高铁维管横联线电流比法供电故障测距工法
22:中国铁建电气化局集团有限公司
23:陈兵杨、毛祖红
24:170
25:250kmh客运专线大坡道双机牵引恒张力放线施工工法
26:中国铁建电气化局集团有限公司
27:董建林、徐光红、白雄雄、王位、魏星
28:171
29:营业线电力电缆桥梁悬挂安装施工工法
30:中国铁建电气化局集团有限公司
31:国金龙、肖环、李春芳、王建东、李照文
32:172
33:自制吊装装置四管通信铁塔组立施工工法
34:中国铁建电气化局集团有限公司
35:王建东、朱春甫、肖环、国金龙、朱卫军
36:173
37:哈佳铁路应答器防冰雪击打装置安装工法
38:中国铁建电气化局集团有限公司
39:李辛亮、杨耀龙、路浩、飞李辛
40:174
41:光缆束管纵剖接续工法
42:中国铁路通信信号上海工程局集团有限公司
43:神凤敏、张健丰、黄健、胡海波、陈国锋
44:175
45:铁路隧道洞室内壁挂式设备安装工厂化预配施工工法
46:通号工程局集团有限公司
47:李国庆、王永哲、刘飞、李博宇、冯冰冰
48:176
49:铁路既有线隧道刚性悬挂接触网精确安装一次到位施工工法
50:通号(长沙)轨道交通控制技术有限公司
51:王清斌、李良、弓晓慧、湛俊、吴伟学'''
def handle():
    text = re.sub(r'\d{1,3}:', '', info_str)
    return text
def print_info(txt):
    count = 0
    for line in txt.split('\n'):
        count += 1
        if re.match(r'\d.*', line) and len(line) < 4:
            print()
            print('%s.'%count, end='')
        else:
            count -= 1
            print(line, end='||')
            # if not re.search(r'.*公司.*分公司', line):
            #     print(line.replace('公司', '公司,'), end='||')
def split_company():
    count = 0
    for line in info_str.split('\n'):
        count += 1
        temp_info = line.split('.')[-1].split('||')[0]
        people = line.split('||')[-2]
        company = temp_info.split('公司')[0] + '公司'
        title = temp_info.split('公司')[-1]
        print('%s.%s||%s||%s' % (count,title, company, people))
if __name__ == "__main__":
    txt = handle()
    print_info(txt)
    # split_company()
    # print(re.sub(r'\d\.', ',', info_str))
