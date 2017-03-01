import requests, urllib, bs4, re, xlwt

#这一步的主要目的是获得网页的Cookie
url = 'http://dean.swjtu.edu.cn/public/QueryStudentInfo.jsp'
r = requests.get(url)

#根据观察，向教务网提交的文件头不变，所以直接将抓包下的文件头复制下来
headers = {
    'Cookie':r.headers['set-cookie'],
    'Referer':'http://dean.swjtu.edu.cn/public/QueryStudentInfo.jsp',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Content-type':'application/x-www-form-urlencoded'  
   }

#这里是打开一个xls文件（还没有保存）
workbook = xlwt.Workbook(encoding='utf-8')

#这里新建一个工作表
sheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)

#这里是记录写文件的行数
row_counter = 0

#这里开始主循环，过程是：
#1. 先构造data然后post 
#2. 获得post后的html文件内容（编码为utf-8），并用BeautifulSoup构造Soup对象（这样方便对html进行解析）
#3. 根据观察，含有检索信息的内容在对"tr"标签的搜索结果列表的倒数第二项，所以直接取出[-2]项
#   并将其内容再作为原始内容生成Soup对象进行二次解析
#4. 将二次解析的Soup的contents提取出来放进info列表，即是最后结果，而后写入打开的工作簿
#5. 全部爬取完毕后保存文件
for id_ in range(2016110001, 2016116389):

    data = {
    "query_action":"query",
    "query_type":"student_id",
    "check_type":"student_id",
    "student_id":str(id_),
    "college_code":"",
    "class_code":"请选择班级"
    }
    #这里提交post请求
    r = requests.post(url, data=urllib.parse.urlencode(data).encode('utf-8'), headers=headers)
    #这里编码为utf-8
    s = r.content.decode('utf-8')
    #这里将html字符串生成为soup对象
    soup = bs4.BeautifulSoup(s, "lxml")
    #这里将搜索到的内容的-2项取出
    raw_info = soup.find_all('tr')[-2]
    #以下就是把信息保存再info中的片段，用try...except是为了防止无关错误使程序中断而得不偿失
    info = []
    try:
        for content in raw_info:
                if content =='\n':
                    continue
                else:
                    info.extend(content.contents)
        print(info)
        for i, j in enumerate(info):
            sheet.write(row_counter, i, j)
        row_counter += 1
    except:
        pass
#最后保存文件
workbook.save('info.xls')
