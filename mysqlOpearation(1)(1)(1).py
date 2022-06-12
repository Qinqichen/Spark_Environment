import MySQLdb
import matplotlib
from pyecharts import options as opts
from pyecharts.charts import Radar
import matplotlib.pyplot as plt
import numpy as np
from pylab import *

#2021年各城市空气质量指标分析镭射图
i = ['太原','大同','吕梁','忻州','朔州','阳泉','晋中','临汾','晋城','长治']
for a in range(len(i)):
    #print(i[a])
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "test", "test", "hadoop_kongqizhiliang")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行SQL语句
    # 数据库操作直接可以读取数据
    # 山西省 11个地级市数据 2021年，2022年得数据基本都有，有几个地级市缺失了一个月得数据，不影响。
    cursor.execute("select AVG(aqi),AVG(pm25),AVG(pm10),AVG(co),AVG(no2),AVG(so2)"
               "from kqzl "
               "where YEAR(date)='2021' && city='%s' " %(i[a]))
    # 使用 fetchone() 方法获取一条数据
    #print(cursor.fetchall())
    i[a]=cursor.fetchall()
    #print(i[a])
    # 关闭数据库连接
    db.close()

c_schema = [
    {"name": "AQI", "max": 150, "min": 5},
    {"name": "PM2.5", "max": 70, "min": 20},
    {"name": "PM10", "max": 150, "min": 5},
    {"name": "CO", "max": 1.5},
    {"name": "NO2", "max": 50},
    {"name": "SO2", "max": 30},
]
c = (
    Radar()
        .add_schema(schema=c_schema, shape="circle")
        .add("太原", i[0], color="#f9713c")
        .add("大同", i[1], color="#7B68EE")
        .add("吕梁", i[2], color="#4B0082")
        .add("忻州", i[3], color="#00BFFF")
        .add("朔州", i[4], color="#3CB371")
        .add("阳泉", i[5], color="#6B8E23")
        .add("晋中", i[6], color="#8B0000")
        .add("临汾", i[7], color="#FF8C00")
        .add("晋城", i[8], color="#008000")
        .add("长治", i[9], color="#2F4F4F")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="2021年度空气质量"))
        .render("radar_air_quality.html")
)
print("镭射图输出成功")

#2021年各城市空气质量指标分析折线图
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 添加这条可以让图形显示中文

x_axis_data = ['AQI','PM2.5','PM10','CO','NO2','SO2']
y_axis_data1 = [i[0][0][0],i[0][0][1],i[0][0][2],i[0][0][3],i[0][0][4],i[0][0][5]]
y_axis_data2 = [i[1][0][0],i[1][0][1],i[1][0][2],i[1][0][3],i[1][0][4],i[1][0][5]]
y_axis_data3 = [i[2][0][0],i[2][0][1],i[2][0][2],i[2][0][3],i[2][0][4],i[2][0][5]]
y_axis_data4 = [i[3][0][0],i[3][0][1],i[3][0][2],i[3][0][3],i[3][0][4],i[3][0][5]]
y_axis_data5 = [i[4][0][0],i[4][0][1],i[4][0][2],i[4][0][3],i[4][0][4],i[4][0][5]]
y_axis_data6 = [i[5][0][0],i[5][0][1],i[5][0][2],i[5][0][3],i[5][0][4],i[5][0][5]]
y_axis_data7 = [i[6][0][0],i[6][0][1],i[6][0][2],i[6][0][3],i[6][0][4],i[6][0][5]]
y_axis_data8 = [i[7][0][0],i[7][0][1],i[7][0][2],i[7][0][3],i[7][0][4],i[7][0][5]]
y_axis_data9 = [i[8][0][0],i[8][0][1],i[8][0][2],i[8][0][3],i[8][0][4],i[8][0][5]]
y_axis_data10 = [i[9][0][0],i[9][0][1],i[9][0][2],i[9][0][3],i[9][0][4],i[9][0][5]]

# plot中参数的含义分别是横轴值，纵轴值，线的形状，颜色，透明度,线的宽度和标签
plt.plot(x_axis_data, y_axis_data1,'ro-', color='#f9713c', alpha=0.8, linewidth=1, label='太原')
plt.plot(x_axis_data, y_axis_data2,'ro-', color='#7B68EE', alpha=0.8, linewidth=1, label='大同')
plt.plot(x_axis_data, y_axis_data3,'ro-', color='#4B0082', alpha=0.8, linewidth=1, label='吕梁')
plt.plot(x_axis_data, y_axis_data4,'ro-', color='#00BFFF', alpha=0.8, linewidth=1, label='忻州')
plt.plot(x_axis_data, y_axis_data5,'ro-', color='#3CB371', alpha=0.8, linewidth=1, label='朔州')
plt.plot(x_axis_data, y_axis_data6,'ro-', color='#6B8E23', alpha=0.8, linewidth=1, label='阳泉')
plt.plot(x_axis_data, y_axis_data7,'ro-', color='#8B0000', alpha=0.8, linewidth=1, label='晋中')
plt.plot(x_axis_data, y_axis_data8,'ro-', color='#FF8C00', alpha=0.8, linewidth=1, label='临汾')
plt.plot(x_axis_data, y_axis_data9,'ro-', color='#008000', alpha=0.8, linewidth=1, label='晋城')
plt.plot(x_axis_data, y_axis_data10,'ro-', color='#2F4F4F', alpha=0.8, linewidth=1, label='长治')
# 显示标签，如果不加这句，即使在plot中加了label='一些数字'的参数，最终还是不会显示标签
plt.legend(loc="upper right")
plt.xlabel('空气质量指标')
plt.ylabel('数值')

plt.show()
# plt.savefig('demo.jpg')  # 保存该图片

print("折线图输出成功")

#山西省21年各市平均aqi指标分析（散点图）
j = ['太原','大同','吕梁','忻州','朔州','阳泉','晋中','临汾','晋城','长治']
for b in range(len(j)):
    #print(i[a])
    # 打开数据库连接
    db = MySQLdb.connect("101.37.145.103", "test", "test", "hadoop_kongqizhiliang")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行SQL语句
    # 数据库操作直接可以读取数据
    # 山西省 11个地级市数据 2021年，2022年得数据基本都有，有几个地级市缺失了一个月得数据，不影响。
    cursor.execute("select AVG(aqi)"
               "from kqzl "
               "where  YEAR(date)='2021' && city='%s' " %(j[b]))
    # 使用 fetchone() 方法获取一条数据
    #print(cursor.fetchall())
    j[b]=cursor.fetchall()
    #print(j[b])
    # 关闭数据库连接
    db.close()

s1 = j[0][0]
s2 = j[1][0]
s3 = j[2][0]
s4 = j[3][0]
s5 = j[4][0]
s6 = j[5][0]
s7 = j[6][0]
s8 = j[7][0]
s9 = j[8][0]
s10 = j[9][0]

font ={'family':'MicroSoft YaHei'} #win可以显示中文
matplotlib.rc("font",**font)

x = ['太原','大同','吕梁','忻州','朔州','阳泉','晋中','临汾','晋城','长治']
y = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10]

plt.scatter(x, y, label='AQI', color='b', marker='*')

plt.xlabel('城市')
plt.ylabel('AQI')
plt.title('Shanxi AQI')
plt.legend()
plt.show()

print("散点图输出成功")


#太原2021年空气质量分析饼状图
# 打开数据库连接
db = MySQLdb.connect("localhost", "test", "test", "hadoop_kongqizhiliang")

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# 使用execute方法执行SQL语句
# 数据库操作直接可以读取数据
# 山西省 11个地级市数据 2021年，2022年得数据基本都有，有几个地级市缺失了一个月得数据，不影响。
cursor.execute("SELECT level as 良 ,COUNT(*) as 次数 "
               "FROM kqzl "
               "WHERE YEAR(date)='2021' && city = '太原' "
               "GROUP BY level")

# 使用 fetchone() 方法获取一条数据
#print(cursor.fetchall())
ty=cursor.fetchall()
#print(ty)
# 关闭数据库连接
db.close()

plt.rcParams['font.sans-serif']=['SimHei']
plt.figure(figsize=(7.5,5),dpi=80) #调节画布的大小
labels = ['良','优','重度污染','严重污染','轻度污染','中度污染'] #定义各个扇形的面积/标签
sizes = [ty[0][1],ty[1][1],ty[2][1],ty[3][1],ty[4][1],ty[5][1]] #各个值，影响各个扇形的面积
colors = ['red','yellowgreen','lightskyblue','yellow','purple','pink'] #每块扇形的颜色
explode = (0.01,0.01,0.01,0.01,0.01,0.01)
patches,text1,text2 = plt.pie(sizes,
                      explode=explode,
                      labels=labels,
                      colors=colors,
                      labeldistance = 1.2,#图例距圆心半径倍距离
                      autopct = '%3.2f%%', #数值保留固定小数位
                      shadow = False, #无阴影设置
                      startangle =90, #逆时针起始角度设置
                      pctdistance = 0.6) #数值距圆心半径倍数距离
#patches饼图的返回值，texts1为饼图外label的文本，texts2为饼图内部文本
plt.axis('equal')
plt.legend()
plt.show()

print("饼状图输出成功")
