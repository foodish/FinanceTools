import os
import requests
import pandas as pd


headers={'User-Agent':'Mozilla 5.0'}


def get_data_and_save(year_month):
    url='http://www.pingan.cn/zh/common/ir/questions-answers/income/%s.shtml?' % year_month
    r=requests.get(url, headers=headers)
    r.encoding='utf-8'
#print(r.text)
    dfs=pd.read_html(r.text)
    for index, df in enumerate(dfs, 1):
        df.to_csv('data/pingan/%s_%s.csv' % (year_month, index), index=False, header=False)
        

def start():      
    try:
        os.makedirs(r'data/pingan')
    except:
        pass  
    year_months=[str(i)+str(j).zfill(2) for i in range(2015, 2018) for j in range(1, 13)]
    for i in year_months:
        print(i)
        get_data_and_save(i)


if __name__ == '__main__':
    #start()
    m = input('enter a month like 201701:')
    get_data_and_save(m)
    