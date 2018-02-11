#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-2-11
# @Author  : foodish
# @File    : 保监会人身保险保费.py
import os
import re
import requests
import pandas as pd


base_url = 'http://www.circ.gov.cn'
first_urls = ['http://www.circ.gov.cn/web/site0/tab5203/module14411/page%d.htm' %d for d in range(1, 12)]
first_url = 'http://www.circ.gov.cn/web/site0/tab5203/module14411/page1.htm'
headers = {'User-Agent':'Mozilla 5.0'}
pattern_url = re.compile(r'<td class="hui14"><span id="lan1"><a href="(.*?)" id="ci[0-9]*" title="(.*?)" target="_blank">', re.S)


def get_page(url):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        r.encoding = 'utf-8'
        return r.text
    else:
        print('网络连接错误')


def get_download_url(html):
    raw_results = re.findall(pattern_url, html)
    results = [(base_url + i, j) for i, j in raw_results]
    return results



def html2csv(html, name):
    dfs = pd.read_html(html, attrs={'id': 'tab_content'}, skiprows=6)
    df = dfs[0]
    df.to_csv(name)


def create_folder():
    try:
        os.mkdir('./data/保监会人身保险保费收入')
    except:
        pass


def get_url_and_doanload(html):
    results = get_download_url(html)
    for download_url, name in results:
        parts = ['data/保监会人身保险保费收入/', name, '.csv']
        csv_path = ''.join(parts)
        print(name)
        if not os.path.exists(csv_path):
            content = get_page(download_url)
            html2csv(content, csv_path)


def first_download():
    create_folder()
    for url in first_urls:
        html = get_page(url)
        get_url_and_doanload(html)


def main():
    create_folder()
    html = get_page(first_url)
    get_url_and_doanload(html)


if __name__ == '__main__':
    # first_download()
    main()