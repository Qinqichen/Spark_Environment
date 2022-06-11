
from hdfs.client import Client#hdfs模块

import os


#得到一个以城市名拼音为键，城市名为名的数据字典，{"ZHENGZHOU":"郑州","KAIFENG":"开封",...}
def get_city_dict(file_path):
    city_dict = {}
    with open(file_path, 'r',encoding='UTF-8') as file:
        #line_list = f.readline()
        for line in file:
            line = line.replace("\r\n", "")
            city_name = (line.split(" ")[0]).strip()
            city_pinyin = ((line.split(" ")[1]).strip()).lower()
            #赋值到字典中...
            city_dict[city_pinyin] = city_name
    return city_dict

file_path = "/root/whether/city.txt"
city_dict = get_city_dict(file_path) #从指定文件city.txt读取城市信息，调用get_city_dict


client = Client("http://127.0.0.1:9870",root='/')#服务器IP,端口，关闭session,避免一直开启

# ls = client.list(hdfs_path='/')

# print(ls)

# client.delete('/tmp/test1',recursive=True)
out =  client.upload("/whether/city.txt",file_path,overwrite=True)#第一个为hadoop中hdfs目录,第二个为文件目录

for city in city_dict.keys() :

    weatherFileName = city+"_weather.csv"

    out =  client.upload("/whether/"+weatherFileName,"/root/whether/"+weatherFileName,overwrite=True)#第一个为hadoop中hdfs目录,第二个为文件目录

    pass 


print("空气质量转存完成")


