# csv文件合并
import os
import pandas as pd


def csv_merge():
    files=os.listdir('data/')
    dirs=['data/'+i for i in files if os.path.isdir('data/'+i)]
    for i in dirs:
        i_files=os.listdir(i)
        csv_files=[i+'/'+j for j in i_files if j.endswith('.csv')]
    #print(csv_files)
        dfs=[pd.read_csv(k, encoding='gbk') for k in csv_files]
        df=pd.concat(dfs)
    #save_path=i+'/'+i.split('/')[-1]+'.csv'
        try:
            os.makedirs('data/'+ i.split('_')[0])
        except:
            pass
        parts=['data/', i.split('_')[0], '/', i, '.csv']
        save_path=''.join(parts)
        print(save_path)
        df.to_csv(save_path, index=False)
