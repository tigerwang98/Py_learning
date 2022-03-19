# encoding: utf-8
"""
@project = Py_learing
@file = test10
@author= wanghu
@create_time = 2021/8/12 11:42
"""
from dateparser import parse
from urllib.parse import quote
from playwright.sync_api import sync_playwright

def handle_page(page):
    page.wait_for_load_state()
    print(page.title())


# print(quote('成都'))
# a中有没有b中的元素，任意一个都可以
# a = ['test', 'asdsa', 'sadasd', 'dddd']
# b = ['this', 'is', 'a', 'test']
# final = [x for x in a if x in b]
# print(final)
with sync_playwright() as p:
    context = p.webkit.launch(headless=False).new_context()
    page_one = context.new_page()
    url = r'http://xypt.mwr.cn/'
    page_one.goto(url)
    page_one.click('xpath=//li[@id="cydw"]')
    page_one.wait_for_timeout(5000)
    all_pages = context.pages
    print(all_pages)
    print(all_pages[1].content())

    page_one.close()
    context.close()
