import os
from openpyxl import load_workbook

def alter(path_list):
    # dir_path = r'C:\Users\123\Desktop\HonorParse\省级\西夏杯\outputfile'
    for data in path_list:
        dir_path = data['path']
        url = data['url']
        filelist = os.listdir(dir_path)
        for file in filelist:
            if file.endswith('xlsx'):
                file_path = dir_path + '\\' + file
                workbook = load_workbook(filename=file_path)
                sheet = workbook.active
                # sheet.insert_cols(idx=12, amount=2)
                rows = 0
                print("当前文件是：", file_path)
                for i in sheet.rows:
                    rows += 1
                # sheet["L1"] = "所属省份的id"
                # sheet["M1"] = "所属城市的id"
                for i in range(2, rows + 1):
                    print('正在修改%s的第%s行' % (file_path, i))
                    # sheet["J"+str(i)] = '宁夏建设工程质量管理协会'
                    sheet["N"+str(i)] = url
                    # sheet["M"+str(i)] = '0'
                    # sheet["E"+str(i)] = '西夏杯（省优质工程）'
                workbook.save(filename=file_path)


if __name__ == "__main__":
    path_list = [
        {'path': r'C:\Users\123\Desktop\4月最后一周\煤炭建设行业QC奖', 'url': 'http://www.cncca.org.cn/CCCA/index.html'},
    ]
    alter(path_list=path_list)
    # temp()