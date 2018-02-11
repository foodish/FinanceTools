#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-2-11
# @Author  : foodish
# @File    : 保监会保费统计.py
import os
import re
import requests
import pandas as pd


base_url = 'http://www.circ.gov.cn'
total_urls = ['http://www.circ.gov.cn/web/site0/tab5201/module14497/page%d.htm' %d for d in range(1, 13)]
life_urls = ['http://www.circ.gov.cn/web/site0/tab5203/module14411/page%d.htm' %d for d in range(1, 12)]
asset_urls = ['http://www.circ.gov.cn/web/site0/tab5202/module14410/page%d.htm' %d for d in range(1, 12)]
area_urls = ['http://www.circ.gov.cn/web/site0/tab5205/module14413/page%d.htm' %d for d in range(1, 9)]
old_urls = ['http://www.circ.gov.cn/web/site0/tab5204/module14412/page%d.htm' %d for d in range(1, 4)]


all_urls = {
    '0':total_urls,  #@todo 无法下载
    '1':life_urls,
    '2':asset_urls,
    '3':area_urls,
    '4':old_urls
}

all_types = {
    '0':'总计',
    '1':'人身',
    '2':'财产',
    '3':'地区',
    '4':'养老'
}

skiprows = {
    '0':5,
    '1':5,
    '2':5,
    '3':5,
    '4':4
}

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


def html2csv(html, name, skip_rows=5):
    dfs = pd.read_html(html, attrs={'id': 'tab_content'}, skiprows=skip_rows)
    df = dfs[0]
    df.to_csv(name)


def create_folder(folder_path):
    try:
        os.makedirs(folder_path)
    except:
        pass
    # try:
    #     os.mkdir('./data/保监会保费收入统计/' + download_type)
    # except:
    #     pass


def get_url_and_doanload(html, folder_path, skiprows):
    results = get_download_url(html)
    for download_url, name in results:
        # result_type = pattern_type.search(name).group()
        # parts = ['data/', '保监会', result_type, '保险保费收入/', name, '.csv']
        name = name.strip()
        parts = [folder_path, '/', name, '.csv']
        csv_path = ''.join(parts)
        # try:
        #     os.mkdir(os.path.dirname(csv_path))
        # except:
        #     pass
        print(name)
        if not os.path.exists(csv_path):
            content = get_page(download_url)
            html2csv(content, csv_path, skiprows)


def first_download(urls, folder_path, skiprows):
    create_folder(folder_path)
    for url in urls:
        html = get_page(url)
        get_url_and_doanload(html, folder_path, skiprows)


def download(url, folder_path, skiprows):
    html = get_page(url)
    get_url_and_doanload(html, folder_path, skiprows)


def main():
    download_type = input('输入保费统计类型：\n1:人身保险；\n2：财产保险；\n3：地区\n4：养老保险')
    folder_name = all_types[download_type]
    skip_rows = skiprows[download_type]
    folder_path = './data/保监会保费统计/' + folder_name
    urls = all_urls[download_type]
    url = urls[0]
    if not os.path.exists(folder_path):
        first_download(urls, folder_path, skip_rows)
    else:
        download(url, folder_path, skip_rows)


if __name__ == '__main__':
    # first_download()
    main()
