#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-09
# @Author  : foodish
# @Email   : xbj1900@gmail.com
# @Link    : https://foodish.github.io
# 获取中证指数官网上的指数行情和指数估值数据
import requests
import csv
import re
import os
from datetime import datetime

headers = {'User-Agent': 'Mozilla 5.0'}
pattern = re.compile(r'"(.*?)"', re.S)
url_gz = 'http://www.csindex.com.cn/data/js/show_zsgz.js?str=ro84Vujt3qqOm29t'
url_hq = 'http://www.csindex.com.cn/data/js/show_zsbx.js?str=tHmi5QqVH3e7EG'
name_gz = 'zsgz.csv'
name_hq = 'zshq.csv'
columns_gz = ('更新日期', '指数简称', '静态市盈率', '滚动市盈率', '市净率', '股息率',
              '去年底静态市盈率', '去年底滚动市盈率', '去年底市净率')
columns_hq = ('更新日期', '指数简称', '收盘', '日涨跌', '日涨跌幅（%）', '今年以来涨跌',
              '今年以来涨跌幅（%）', '成交额较昨日增减（亿元）', '成交额较昨日增减（%）')


def create_folder():
    try:
        os.mkdir('./data')
    except:
        pass


def get_is_open():
    csv_dict = {}
    today = datetime.strftime(datetime.today(), '%Y-%m-%d')
    with open(r'data/trade_cal_2018.csv') as f:
        for line in f:
            line_date, is_open = line.strip().split(',')
            csv_dict[line_date] = is_open
    return csv_dict[today]
    
    
def download_index_info_first(url, name, columns):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        r.encoding = 'gbk'
        all_data = re.findall(pattern, r.text)
        update_time = all_data[0]
        total_num = len(all_data)
        row = total_num // 9

        with open('data/' + name, 'w', newline='') as f:
            ff = csv.writer(f)
            ff.writerow(columns)
            for j in range(0, row):
                tmp = [all_data[i] for i in range(1 + j * 9, 10 + j * 9)]
                tmp.insert(0, update_time)
                ff.writerow(tuple(tmp))
    else:
        print('网络连接错误')


def download_index_info(url, name):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        r.encoding = 'gbk'
        all_data = re.findall(pattern, r.text)
        update_time = all_data[0]
        total_num = len(all_data)
        row = total_num // 9

        with open('data/' + name, 'a', newline='') as f:
            ff = csv.writer(f)
            # ff.writerow(columns)
            for j in range(0, row):
                tmp = [all_data[i] for i in range(1 + j * 9, 10 + j * 9)]
                tmp.insert(0, update_time)
                ff.writerow(tuple(tmp))
    else:
        print('网络连接错误')


def main():
    create_folder()
    # download_index_info_first(url_gz, name_gz, columns_gz)
    # download_index_info_first(url_hq, name_hq, columns_hq)
    download_index_info(url_gz, name_gz)
    download_index_info(url_hq, name_hq)


if __name__ == '__main__':
    if get_is_open() == 1:
        main()
