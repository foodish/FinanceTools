import os
import requests
import pandas as pd


headers={'User-Agent':'Mozilla 5.0'}


def get_data_and_save(year_month):
    '''
    获取中国平安规模保费数据并保存为csv文件
    :param year_month:形如'201801'表示18年1月份数据
    :return:
    '''
    url='http://www.pingan.cn/zh/common/ir/questions-answers/income/%s.shtml?' % year_month
    r=requests.get(url, headers=headers)
    r.encoding='utf-8'
#print(r.text)
    dfs=pd.read_html(r.text)
    for index, df in enumerate(dfs, 1):
        df.to_csv('data/pingan/%s_%s.csv' % (year_month, index), index=False, header=False, encoding='utf_8_sig')
        

def start():
    '''
    下载中国平安历史规模保费数据，只需要第一次使用，后续只需下载每月数据即可
    :return:
    '''
    try:
        os.makedirs(r'data/pingan')
    except:
        pass  
    year_months=[str(i)+str(j).zfill(2) for i in range(2015, 2019) for j in range(1, 13)]
    for i in year_months:
        try:
            get_data_and_save(i)
            print(i)
        except:
            pass


if __name__ == '__main__':
    #start()  #第一次使用
    m = input('enter a month like 201701:')
    get_data_and_save(m)
    