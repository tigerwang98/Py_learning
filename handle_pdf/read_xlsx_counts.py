import os
from openpyxl import load_workbook
dir_path = r'C:\Users\123\Desktop\补漏荣誉\安装协会科学技术进步奖'
# dir_path = r'C:\Users\123\Desktop\HonorParse\企业荣誉\国家级\煤炭建设行业QC奖\outputfile'
filelist = os.listdir(dir_path)
count = 0
for file in filelist:
    if file.endswith('xlsx'):
        file_path = dir_path + '\\' + file
        print("当前的文件是：", file_path)
        workbook = load_workbook(filename=file_path)
        sheet = workbook.active
        for i in sheet.rows:
            count += 1
print("总共%s条"%count)

