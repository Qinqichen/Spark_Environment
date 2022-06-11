import MySQLdb



# 打开数据库连接
db = MySQLdb.connect("101.37.145.103", "test", "test", "hadoop_kongqizhiliang")

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# 使用execute方法执行SQL语句
# 数据库操作直接可以读取数据
# 山西省 11个地级市数据 2021年，2022年得数据基本都有，有几个地级市缺失了一个月得数据，不影响。
cursor.execute("select date, aqi,aqiarrange,level,pm25 from kqzl where city='晋中' and date < '2021-06-09'  ;")

fk = cursor.fetchall()

for i in range(len(fk)) :
    tr = "<tr>"
    for j in range(len(fk[i])):
        tr= tr +"<td>{}</td>".format(str(fk[i][j]))
    tr = tr + "</tr>"

    print(tr)





# print(len(fk))

# print(fk)

# 使用 fetchone() 方法获取一条数据


# 关闭数据库连接
db.close()