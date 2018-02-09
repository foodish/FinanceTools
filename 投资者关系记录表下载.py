#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-06
# @Author  : foodish
# @Email   : xbj1900@gmail.com
# @Link    : https://foodish.github.io
# 投资者关系记录表下载：
# 002508：老板电器
# 002415：海康威视
import requests
import re
import os
import time
# from tqdm import tqdm


base_url = 'http://www.cninfo.com.cn'
tzz_url = 'http://www.cninfo.com.cn/search/tzzfulltext.jsp'
headers = {'User-Agent': 'Mozilla/5.0'}
pattern_code = re.compile(pattern='[0-9]{6}')
pattern_url = re.compile(
    r'<td class="qsgg"><a href="(.*?)" target=new>(.*?)</a>', re.S)
pattern_file = re.compile(r'.(DOC|PDF|DOCX|doc|pdf|docx)', re.S)


def get_stock_code():
    input_result = input('请输入一个六位数股票代码：\n')
    while True:
        if pattern_code.match(input_result) and len(input_result) == 6:
            secCode = input_result
            # print('输入成功，开始下载。。。。。。')
            break
        else:
            input_result = input('输入错误，请重新输入:')
    return secCode


def get_download_info(secCode='002415', today='2018-02-06', pageNo='1'):
    params = {
        'orderby': 'date11',
        'startTime': '2010-01-01',
        'endTime': today,
        'stockCode': secCode,
        'pageNo': pageNo
    }
    r = requests.post(tzz_url, headers=headers, params=params)
    results = re.findall(pattern_url, r.text)

    return results


def create_folder():
    try:
        os.mkdir('/tzz_data')
    except:
        pass
    # if os.path.exists(r'./data'):
    # if os.path.exists(r'./ttz_data'):
    #     pass
    # else:
    #     # os.mkdir(r'./data')
    #     os.mkdir(r'./tzz_data')
    return


def start_download(results):
    for adjUrl, name in results:
        download_url = base_url + adjUrl
        r = requests.get(download_url, headers=headers)
        print(download_url)
        fileType = pattern_file.search(adjUrl).group()
        parts = ['tzz_data/', name, fileType]
        file_path = ''.join(parts)
        print(r.status_code)
        if r.status_code == 200:
            print(r.headers)
            print('正在下载：', file_path[9:])
            with open(file_path, 'wb') as f:
                f.write(r.content)


def main():
    code = get_stock_code()
    today = time.strftime("%Y-%m-%d")
    create_folder()
    for i in range(1, 4):
        try:
            results = get_download_info(code, today, str(i))
            start_download(results)
        except:
            pass


def test():
    code = '002508'
    today = '2018-02-08'

    for i in range(1, 4):
        results = get_download_info(code, today, '1')
        start_download(results)


if __name__ == '__main__':
    main()
    # test()