from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkConf
import MySQLdb



sc = SparkContext()

sc = SparkSession.builder \
    .master("local") \
    .appName("山西省空气质量分析") \
    .getOrCreate()


sqlcontext = SQLContext(sc)

#format后面为告诉程序读取csv格式,load后面为hdfs地址,hdfs后面跟着hadoop的名字,然后文件目录(这块有点懵,如果报错,跟着报错查修)
# data = sqlcontext.read.format("com.databricks.spark.csv").\
#         options(header="true",inferschema="true").\
#         load("http://127.0.0.1:9870/test1/5min.csv")


data_txt = sc.read.text('/whether/city.txt')

# for i in range(data_txt.count()):

#     print(data_txt.iloc[i])

def getMySqlConnect(ip,user,password,database):

    # 打开数据库连接
    db = MySQLdb.connect(ip,user,password,database,charset='utf8')

    return db

def data_process(data):
    data = data.value.split(' ')
    city_chinese = data[0]
    city_pinyin = data[1]

    file_name = city_pinyin+"_weather.csv"

    data_csv = sc.read.csv('/whether/'+file_name,header=True)

    saveToMysql(city_pinyin=city_pinyin, city_chinese=city_chinese, data=data_csv)


def concatInsertSql(city_pinyin , city_chinese,data):

    # print(data)

    id = city_pinyin + '-' + data['date']

    columns = ['date','level','AQI','AQIarrange','PM25','PM10','So2','No2','Co','O3']

    sub = []

    for column in columns :
        sub.append(data[column])
    
    sub[0] = "'" + sub[0] + "'"
    sub[1] = "'" + sub[1] + "'"
        

    sub = ','.join(sub)

    # print(sub)

    insertSql = "insert into kqzls values ('{}',{},'{}');".format(id,sub,city_chinese)

    return insertSql



def saveToMysql(city_pinyin , city_chinese,data):

    db = getMySqlConnect("101.37.145.103", "test", "test", "hadoop_kongqizhiliang")

    cursor = db.cursor()
    cursor.execute("SET NAMES utf8")

    data = data.toPandas()

    data.columns = ['date','level','AQI','AQIarrange','PM25','PM10','So2','No2','Co','O3']

    data_len = data.shape[0]

    for i in range(data_len) :
        sub_data = data.loc[i]  

        insertSql = concatInsertSql(city_pinyin, city_chinese, sub_data)

        if i % 100 == 0 :

            print("{} 已完成 {}/{} ".format(city_chinese,str(i),str(data_len)))



        try:
            a = cursor.execute(insertSql)
            db.commit()
            # print(a)

        except Exception():
            db.rollback()


data_len = data_txt.count()

data_txt = data_txt.toPandas()

for i in range(data_len):

    data_process(data_txt.loc[i])

    print("{} 完成推送！".format(data_txt.loc[i]))





sc.stop()





