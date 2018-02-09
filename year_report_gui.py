#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-2-9
# @Author  : foodish
# @File    : year_report_gui.py
import tkinter
import urllib.request
import urllib.parse
import json
import re
from os import mkdir
from os.path import exists
import time


pattern = re.compile(pattern='[0-9]{6}')
headers = {'User-Agent': 'Mozilla/5.0'}
base_url = 'http://www.cninfo.com.cn/'
query_url = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'

time1 = 0
time2 = 0
time3 = 0
time4 = 0

task = tkinter.Tk()

task.title('A股年报下载器')
# task.geometry('800x600')

label = tkinter.Label(task, text = '股票代码：')
label.grid(row = 0, sticky = tkinter.W)

entry = tkinter.Entry(task)
entry.grid(row = 0, column = 1, sticky = tkinter.E)

show_info = tkinter.Label(task, text = '')
show_info.grid(row = 4, column = 0, sticky = tkinter.W)

def get_stock_code():
    s1 = entry.get()
    t1 = len(s1)
    if len(s1) == 6:
        show_info['text'] = '下载进度'
    else:
        show_info['text'] = '输入错误'
        entry.delete(0, t1)
    return s1


def select_nb():
    global time1
    if time1 % 2 != 0:
        time1 += 1
        return 'category_ndbg_szsh;'
    else:
        time1 += 1
        return ''


def select_bnb():
    global time2
    if time2 % 2 != 0:
        time2 += 1
        return 'category_bndbg_szsh;'
    else:
        time2 += 1
        return ''

def select_yjb():
    global time3
    if time3 % 2 != 0:
        time3 += 1
        return 'category_yjdbg_szsh;'
    else:
        time3 += 1
        return ''


def select_sjb():
    global time4
    if time4 % 2 != 0:
        time4 += 1
        return 'category_sjdbg_szsh;'
    else:
        time4 += 1
        return ''


label = tkinter.Label(task, text = '财报类型：')
label.grid(row = 1, sticky = tkinter.W)


check_nb = tkinter.Checkbutton(task, text = '年报', command = select_nb)
check_nb.grid(row = 2, column = 0)
check_bnb = tkinter.Checkbutton(task, text = '半年报', command = select_bnb)
check_bnb.grid(row = 2, column = 1)
check_yjb = tkinter.Checkbutton(task, text = '一季报', command = select_yjb)
check_yjb.grid(row = 3, column = 0)
check_sjb = tkinter.Checkbutton(task, text = '三季报', command = select_sjb)
check_sjb.grid(row = 3, column = 1)


def get_category():
    s1 = select_nb()
    s2 = select_bnb()
    s3 = select_yjb()
    s4 = select_sjb()
    parts = [s1, s2, s3,s4]
    category = ''.join(parts)
    return category


def get_download_url(stock_code, category='category_ndbg_szsh', pageNum = '1', pageSize = '50'):
    params = {'stock': stock_code,
              # category_ndbg_szsh;category_bndbg_szsh;category_yjdbg_szsh;category_sjdbg_szsh;category_scgkfx_szsh;
              'category': category,
              'pageNum': pageNum,
              'pageSize': pageSize,
              'column': 'sse',  # 还有个szse_sme,为深市，不过测试002508也没问题
              'tabName': 'fulltext'
              }
    data = bytes(urllib.parse.urlencode(params), encoding='utf-8')
    req = urllib.request.Request(
        url=query_url, data=data, headers=headers, method='POST')
    r = urllib.request.urlopen(req)
    # print(r.read().decode('utf-8'))
    stock_data = json.loads(r.read())
    # print(stock_data)
    announcements = stock_data['announcements']
    total_num = stock_data['totalRecordNum']
    total_page = int(total_num) // int(pageSize) + 1
    results = [i for i in announcements if '摘要' not in i['announcementTitle']]

    download_and_save_paths = []
    # for i in tqdm(results):
    for i in results:
        secName = i['secName']
        announcementTitle = i['announcementTitle']
        # adjunctType = i['adjunctType']
        adjunctUrl = i['adjunctUrl']
        download_url = base_url + adjunctUrl
        if announcementTitle.startswith(secName):
            parts = ['data/', announcementTitle, '.pdf']
        else:
            parts = ['data/', secName, announcementTitle, '.pdf']
        # file_path = r'data/' + announcementTitle + '.pdf'
        file_path = ''.join(parts)
        item = (download_url, file_path)
        download_and_save_paths.append(item)

    return download_and_save_paths, total_page


def change_schedule(now_schedule, all_schedule):
    frame = tkinter.Frame(task).grid(row=5, column=0)
    canvas = tkinter.Canvas(frame, width=120, height=30, bg='white')
    out_rec = canvas.create_rectangle(5, 5, 105, 25, outline='blue', width=1)
    fill_rec = canvas.create_rectangle(5, 5, 5, 25, outline='', width=0, fill='blue')
    canvas.coords(fill_rec, (5,5,6 + (now_schedule/all_schedule)*100,25))
    canvas.grid(row=5, column=0)
    task.update()
    x = tkinter.StringVar()
    tkinter.Label(frame, textvariable=x).grid(row=5, column=1)

    x.set(str(round(now_schedule/all_schedule*100, 2)) + '%')
    if round(now_schedule/all_schedule*100, 2) == 100.00:
        x.set('下载完成')


def download_and_save(download_and_save_paths):
    num = len(download_and_save_paths)
    i = 0
    for download_url, file_path in download_and_save_paths:
        # file_content = requests.get(download_url, headers=headers)
        # print('正在下载：', file_path[5:])
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(download_url, file_path)
        i = i + 1
        change_schedule(i, num)
        # time.sleep(500)


def create_folder():
    # if os.path.exists(r'./data'):
    if exists(r'./data'):
        pass
    else:
        # os.mkdir(r'./data')
        mkdir(r'./data')
    return


def main():
    secCode = get_stock_code()
    category = get_category()
    # print('====开始下载====')
    page_size = '30'
    download_and_save_paths, total_page = get_download_url(secCode, category, '1', page_size)
    create_folder()
    if total_page == 1:
        download_and_save(download_and_save_paths)
    else:
        download_and_save(download_and_save_paths)
        # time.sleep(500)
        for page in range(2, total_page + 1):
            url_and_paths, _ = get_download_url(secCode, category, str(page), page_size)
            download_and_save(url_and_paths)
            # time.sleep(500)
    # print('====下载完毕====')


button = tkinter.Button(task, text='开始下载', command=main)
button.grid(row=4, column=1, sticky=tkinter.E)


if __name__ == '__main__':
    task.mainloop()
    # main()
    # test()
    # input()
# 以下语句可防止pyinstaller打包后的exe运行闪退
# time.sleep(50)
