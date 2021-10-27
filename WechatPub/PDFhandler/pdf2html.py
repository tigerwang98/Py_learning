import subprocess
import os
import sys
import importlib
import time
import requests
importlib.reload(sys)
from pdfminer.pdfparser import PDFParser, PDFDocument
#from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pydocx import PyDocX
# from win32com import client as wc

class PDFtranslator():
    '''
    pdf转换器
    '''
    def __init__(self):
        # self.current_path = os.path.dirname(__file__) + '\\'
        self.current_path = os.path.dirname(__file__) + '\\' #当前文件路径
        self.current_object_path = os.getcwd()+'\\' #当前调用对象路径
        # self.current_path = ''
        self.pdf_download_html = '''
        <a href="{pdf_download_url}">点击查看</a><br>
        '''
    def download(self, filename, download_url):
        '''下载文件函数'''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }
        req = requests.get(download_url, headers=headers)
        res = req.content
        with open(filename, 'wb') as f:
            f.write(res)
        return res

    def pdf2html_procing(self, pdffilename, pdf_url, encoding='utf-8'):
        '''
        PDF向HTML转换函数
        :param
        pdffilename: pdf文件名，一般不用变化，因为会自动删除
        pdf_url：PDF的下载地址
        encoding：编码方式，根据转换结果选取
        '''
        t1 = time.time()
        if pdf_url:
            try:
                self.download(pdffilename, pdf_url)
            except Exception as e:
                print('文件下载失败,\n %s'%e)
                return
            print('************文件下载完成，现在开始转换********')
        output_filename = pdffilename.replace('.pdf', '.html')
        t1 = time.time()
        print(3333333,self.current_path)
        subprocess.call(self.current_path+"pdf2htmlEX-win32-0.14.6-with-poppler-data\pdf2htmlEX.exe --embed-css 0 --embed-javascript 0 --embed-font 1 --dest-dir ./output1023 {pdffilename} {output_filename}".format(pdffilename=pdffilename, output_filename=output_filename),shell=True)
        # subprocess.call(self.current_path+"pdf2htmlEX-win32-0.14.6-with-poppler-data\pdf2htmlEX.exe --embed-image 1 --embed-css 0 --embed-font 1 --embed-javascript 0 --embed-outline 0 --no-drm 0 --dest-dir ./output0928 {pdffilename} {output_filename}".format(pdffilename=pdffilename, output_filename=output_filename),shell=True)
        print('用时：',time.time()-t1)
        os.remove(pdffilename)
        try:
            with open('./output1023/'+output_filename, 'r', encoding=encoding, errors='ignore') as f:
                res = f.read()
            import shutil
            shutil.rmtree('./output1023/')
            # os.removedirs('./output1023/')
        except:
            print('pdf2htmlEX转换文件失败！用时:',time.time()-t1)
            return None
        # print(res)
        print('pdf转换用时:', time.time()-t1)
        return res

    def pdf2html(self, pdffilename='test.pdf', pdf_url=None):
        try:
            res = self.pdf2html_procing(pdffilename=pdffilename,pdf_url=pdf_url)
            return res
        except Exception as e:
            print('pdf2text转换失败：',str(e))
            return ''

    # 解析pdf文件函数
    def pdf2text_procing(self, pdffilename, pdf_url):
        '''
        解析pdf文件，将pdf转换为text
        '''
        if pdf_url:
            try:
                self.download(pdffilename, pdf_url)
            except Exception as e:
                print('pdf文件下载失败,\n %s'%e)
                return
            print('pdf文件下载完成，现在开始转换')
        fp = open(pdffilename, 'rb')  # 以二进制读模式打开
        # 用文件对象来创建一个pdf文档分析器
        parser = PDFParser(fp)
        # 创建一个PDF文档
        doc = PDFDocument()
        # 连接分析器 与文档对象
        parser.set_document(doc)
        try:
            doc.set_parser(parser)
        except:
            print('not pdf file!')
            return

        # 提供初始化密码
        # 如果没有密码 就创建一个空的字符串
        doc.initialize()

        # 检测文档是否提供txt转换，不提供就忽略
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            # 创建PDf 资源管理器 来管理共享资源
            rsrcmgr = PDFResourceManager()
            # 创建一个PDF设备对象
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            # 创建一个PDF解释器对象
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            # 用来计数页面，图片，曲线，figure，水平文本框等对象的数量
            num_page, num_image, num_curve, num_figure, num_TextBoxHorizontal = 0, 0, 0, 0, 0
            contents = ''
            # 循环遍历列表，每次处理一个page的内容
            for page in doc.get_pages():  # doc.get_pages() 获取page列表
                num_page += 1  # 页面增一
                interpreter.process_page(page)
                # 接受该页面的LTPage对象
                layout = device.get_result()
                for x in layout:
                    if isinstance(x, LTImage):  # 图片对象
                        num_image += 1
                    if isinstance(x, LTCurve):  # 曲线对象
                        num_curve += 1
                    if isinstance(x, LTFigure):  # figure对象
                        num_figure += 1
                    if isinstance(x, LTTextBoxHorizontal):  # 获取文本内容
                        num_TextBoxHorizontal += 1  # 水平文本框对象增一
                        contents += x.get_text()+'<br>'

            print('对象数量：\n', '页面数：%s\n' % num_page, '图片数：%s\n' % num_image, '曲线数：%s\n' % num_curve, '水平文本框：%s\n'
                  % num_TextBoxHorizontal, )
            return contents

    def pdf2text(self, pdffilename='text.pdf', pdf_url=None):
        try:
            res = self.pdf2text_procing(pdffilename=pdffilename,pdf_url=pdf_url)
            os.remove(pdffilename)
            return res
        except Exception as e:
            print('pdf2text转换失败：',str(e))
            os.remove(pdffilename)


    def doc2docx(self, doc_name):
        """
        :doc转docx
        ：doc_name: doc文件名
        """
        import pythoncom
        pythoncom.CoInitialize()
        word = wc.Dispatch("Word.Application")
        # 寻找文件的绝对路径,因为Open方法必须要绝对路径才能找到文件
        # dir_path = os.path.abspath(os.path.split(__file__)[0])
        # docpath = os.path.join(dir_path, doc_name)
        # 打开doc文件
        # doc = word.Documents.Open(docpath)
        doc = word.Documents.Open(doc_name)
        # 使用参数16表示将doc转换成docx
        # doc.SaveAs(docpath + 'x', 16)
        doc.SaveAs(doc_name + 'x', 16)
        # 一定要退出，因为这里相当于打开了office应用，不退出的话会报错
        doc.Close()
        word.Quit()

    def doc_or_docx2html(self, docfilename, doc_url=None):
        '''
        参数：
            docfilename: doc文件名(绝对路径)
            doc_url：doc文件的网络url
            :return: html文件内容
        '''
        docfilename = self.current_object_path+docfilename
        print(docfilename,docfilename.split('\\')[-1])
        if doc_url:
            try:
                self.download(docfilename, doc_url)
            except Exception as e:
                print('下载doc文件时发生错误:%s, 退出！' % e)
                return doc_url
        if 'x' in docfilename.split('\\')[-1]:
            #  利用PyDocx转换成html
            html = PyDocX.to_html(docfilename)
            os.remove(docfilename)
        else:
            print('ubantu下暂时无法处理doc文件！')
            html = doc_url
            #  在此将doc转为docx
            # self.doc2docx(docfilename)
            # time.sleep(2)
            # html = PyDocX.to_html(docfilename + 'x')
            # os.remove(docfilename + 'x')
            # os.remove(docfilename)
        print('doc文件转换HTML成功!')
        return html


if __name__ == '__main__':
    pdfhandler = PDFtranslator()
    url = 'http://zbtb.gd.gov.cn/platform/attach/download?id=78c67e0dad804f38a010cfc941910793'
    # pdfhandler = PDFtranslator()
    ret = pdfhandler.doc_or_docx2html('test.doc', doc_url=url)
    print(ret)
