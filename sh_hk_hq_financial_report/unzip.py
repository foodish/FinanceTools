#zip文件解压缩并删除原压缩文件
#巨潮下载三表和行情为压缩文件
import zipfile  
import os


def un_zip(file_name):  
    """unzip zip file"""  
    zip_file = zipfile.ZipFile(file_name)  
    if os.path.isdir(file_name[:-4]):  
        pass  
    else:  
        os.mkdir(file_name[:-4])  
    for names in zip_file.namelist():  
        zip_file.extract(names, file_name[:-4])  
    zip_file.close()
    
def unzip_all():      
    files=os.listdir('data/')  
    zip_files=[i for i in files if     i.endswith('.zip')]
    for i in zip_files:
        un_zip('data/'+i)
        os.remove('data/'+i)


if __name__ == '__main__':
    unzip_all()