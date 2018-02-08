#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-2-8
# @Author  : foodish
# @File    : A股港股三表+行情数据下载.py
# 从巨潮下载A股、港股三表数据及行情
import requests
# import time


query_a = 'http://www.cninfo.com.cn/cninfo-new/data/query'
query_hk = 'http://www.cninfo.com.cn/cninfo-new/data/queryhk'
download_url = 'http://www.cninfo.com.cn/cninfo-new/data/download'
headers = {'User-Agent': 'Mozilla/5.0'}
# params = {
#     'code':'02319',  #‘600276
#     'market':'hk', #hk港股；sh上证；sz深证
#     'orgid':'gshk0002319',  # gssh0600276；9900012688；9900008689
#     'type':'lrb',  #fzb负债表;lrb利润表；llb现金流量表;hq行情
#     'minYear':'2000', #2000
#     'maxYear':'2018', #2018
# }


market_dict = {
    '1': query_a,
    '2':query_hk
}


data_type_dict = {
    '1':'lrb',
    '2':'fzb',
    '3':'llb',
    '4':'hq'
}


def get_market_type_url():
    market_type = input('''
    请选择股票市场类型：
    ===================
    1：A股；
    2：港股
    ===================
    ''')
    url = market_dict[market_type]
    return url


def get_stock_code():
    code = input('请输入要下载的股票代码：\n')
    return code


def get_data_type():
    data_type_input = input('''
    请选择下载的数据类型：
    ===================
    1：利润表；
    2：资产负债表；
    3：现金流量表；
    4：股票行情数据
    ===================
    ''')
    data_type = data_type_dict[data_type_input]
    return data_type


def query(url, keyword):
    query_data = {
        'hq_or_cw': '2',
        'keyWord' : keyword,
        'maxNum'  : '10'
    }

    r = requests.post(url, data=query_data, headers=headers)
    if r.status_code == 200:
        results = r.json()[0]
        startTime = results['startTime']
        orgId = results['orgId']
        category = results['category']
        market = results['market']
        code = results['code']
        # pinyin = results['pinyin']
        zwjc = results['zwjc']
        stock_info = (startTime, orgId, category, market, code, zwjc)
        return stock_info
    else:
        print('网络连接错误！')


def download(query_data, data_type):
    startTime, orgId, category, market, code, zwjc = query_data
    params = {
        'code'   : code,
        'market' : market,
        'orgid'  : orgId,
        'type'   : data_type,  # fzb负债表;lrb利润表；llb现金流量表;hq行情
        'minYear': startTime,
        'maxYear': '2018',
    }
    r = requests.post(download_url, data=params, headers=headers)
    if r.status_code == 200:
        # print(r.headers)
        parts = [code, '_', zwjc, '_', data_type, '_', startTime, '_', '2018', '.zip']
        filename = ''.join(parts)
        with open('data/' + filename, 'wb') as f:
            f.write(r.content)
    else:
        print('网络连接错误')


def test():
    stock_query_url = query_a
    stock_code = '600519'
    data_type = 'hq'
    query_info = query(stock_query_url, stock_code)
    print('正在下载', query_info[5], '的数据')
    download(query_info, data_type)
    print('下载完毕')


def main():
    stock_query_url = get_market_type_url()
    stock_code = get_stock_code()
    query_info = query(stock_query_url, stock_code)
    print('开始下载', query_info[5], '的三表和行情数据')
    # ask_for_type = input()
    # data_type = get_data_type()
    data_types = ['lrb', 'fzb', 'llb', 'hq']
    for data_type in data_types:
        download(query_info, data_type)
    print('下载完毕')


if __name__ == '__main__':
    main()