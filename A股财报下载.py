#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-02-07
# @Author  : foodish
# @Email   : xbj1900@gmail.com
# @Link    : https://foodish.github.io
# 下载巨潮年报等；为便于pyinstaller打包未采用第三方模块如requests
import urllib.request
import urllib.parse
import json
import re
from os import mkdir
from os.path import exists


pattern = re.compile(pattern='[0-9]{6}')
headers = {'User-Agent': 'Mozilla/5.0'}
base_url = 'http://www.cninfo.com.cn/'
query_url = 'http://www.cninfo.com.cn/cninfo-new/announcement/query'
category_list = {
    '0': 'category_ndbg_szsh;',  # 年度报告
    '1': 'category_bndbg_szsh;',  # 半年度报告
    '2': 'category_yjdbg_szsh;',  # 一季度报告
    '3': 'category_sjdbg_szsh;',  # 三季度报告
    '4': 'category_scgkfx_szsh;',  # 首次公开发行
    'all': '0'  # 所有类型报告
}
'''[各种类型公告]
    category_ndbg_szsh;年度报告
    category_bndbg_szsh;半年度报告
    category_yjdbg_szsh;一季度报告
    category_sjdbg_szsh;三季度报告
    category_scgkfx_szsh;首次公开发行
    category_zf_szsh;增发
    category_kzhz_szsh;可转换债券
    category_zqgg_szsh;债券公告
    category_qtrz_szsh;特别融资
    category_pg_szsh;配股
    category_zjjg_szsh;特别机构报告
    category_tzzgx_szsh;投资者关系
    category_qtzdsx_szsh;其他重大事项
[description]
'''


def get_stock_code():
    input_result = input('请输入一个六位数股票代码：\n')
    while True:
        if pattern.match(input_result) and len(input_result) == 6:
            secCode = input_result
            # print('输入成功，开始下载。。。。。。')
            break
        else:
            input_result = input('输入错误，请重新输入:')
    return secCode


def get_category():
    input_result = input('请输入要下载的财报类型：\n0表示年报\n1表示半年报\n2表示一季报\n3表示三季报\n')
    while True:
        if input_result in ['0', '1', '2', '3']:
            category = category_list[input_result]
            break
        else:
            input_result = input('请重新输入：')
    return category


def get_download_url(stock_code, category='category_ndbg_szsh'):
    '''[获取历年财报的下载网址]

    [description]

    Returns:
        [数组] -- [返回数组类型，数组中元素为元组形式，其中保存了下载网址和保存路径]
    '''
    params = {'stock': stock_code,
              # category_ndbg_szsh;category_bndbg_szsh;category_yjdbg_szsh;category_sjdbg_szsh;category_scgkfx_szsh;
              'category': category,
              'pageNum': '1',
              'pageSize': '50',
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
    results = [i for i in announcements if '摘要' not in i['announcementTitle']]

    download_and_save_paths = []
    # for i in tqdm(results):
    for i in results:
        secName = i['secName']
        announcementTitle = i['announcementTitle']
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

    return download_and_save_paths


def download_and_save(download_and_save_paths):
    for download_url, file_path in download_and_save_paths:
        # file_content = requests.get(download_url, headers=headers)
        print('正在下载：', file_path[5:])
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(download_url, file_path)


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
    print('====开始下载====')
    download_and_save_paths = get_download_url(secCode, category)
    create_folder()
    download_and_save(download_and_save_paths)
    print('====下载完毕====')


def test():
    secCode = '600519'
    category = 'category_ndbg_szsh;'
    print('====开始下载====')
    download_and_save_paths = get_download_url(secCode, category)
    create_folder()
    download_and_save(download_and_save_paths)
    print('====下载完毕====')


if __name__ == '__main__':
    main()
    # test()
    input()
# 以下语句可防止pyinstaller打包后的exe运行闪退
# time.sleep(50)
