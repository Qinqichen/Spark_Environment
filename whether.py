import io
import sys
import requests
import os
import bs4
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

# target_year_list = ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018","2019"]
target_year_list = [ "2021" , "2022"]
target_month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

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

file_path = "./whether/city.txt"
city_dict = get_city_dict(file_path) #从指定文件city.txt读取城市信息，调用get_city_dict

# print(city_dict)

#得到全部url，格式：url = "http://www.tianqihoubao.com/lishi/beijing（城市名）/month/201812（年月).html"
def get_urls(city_pinyin):
    urls = []
    for year in target_year_list:
        for month in target_month_list:
            date = year + month
            urls.append("http://www.tianqihoubao.com/aqi/{}-{}.html".format(city_pinyin, date))#每年每月每个地市
    return urls

#用BeautifulSoup解析每个url返回的网页，以得到有用的数据
def get_soup(url): 
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()  # 若请求不成功,抛出HTTPError 异常
        # r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, "html.parser")
        return soup
    # except HTTPError:
    #  return "Request Error"
    except Exception as e:
        print(e)
        pass

#保存解析后的网页数据
def get_data(url):
    print(url)
    try:
        soup = get_soup(url)

        all_weather = soup.find('div', class_="api_month_list").find('table').find_all("tr")
        data = list()
        for tr in all_weather[1:]:
            td_li = tr.find_all("td")
            for td in td_li:
                s = td.get_text()
                # print(s.split())
                data.append("".join(s.split()))

        # print(data)
        res = np.array(data).reshape(-1, 10)
        return res
    except Exception as e:
        print(e)
        pass

#数据保存到本地csv文件
def saveTocsv(data, city):
    '''
    将天气数据保存至csv文件
    '''
    fileName = './whether/' + city + '_weather.csv'
    result_weather = pd.DataFrame(data, columns=['date','level','AQI','AQIarrange','PM25','PM10','So2','No2','Co','O3'])
    # print(result_weather)
    result_weather.to_csv(fileName,index=False, header=(not os.path.exists(fileName))) #mode='a'追加
    print('Save all weather success!')

#主函数
if __name__ == '__main__':
    for city in city_dict.keys(): #读城市字典的键
        # print(city, city_dict[city])
        data_ = list()

        urls = get_urls(city) #urls保存了所有城市的所有年月的url

        for url in urls:
            try:
                new_data = get_data(url)
                # if len(new_data) == 0 :
                #     break
                data_.extend(new_data)  # 列表合并，将某个城市所有月份的天气信息写到data_
            except Exception as e:
                print(e)
                pass
        saveTocsv(data_, city)  # 保存为csv
