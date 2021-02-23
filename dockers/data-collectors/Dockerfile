FROM docker.io/python:3.8-slim-buster

# https://opsx.alibaba.com/mirror
# 使用阿里云镜像地址。修改debian apt 更新地址，pip 地址，设置时区。
RUN echo  "deb http://mirrors.aliyun.com/debian/ buster main non-free contrib\n\
deb-src http://mirrors.aliyun.com/debian/ buster main non-free contrib\n\
deb http://mirrors.aliyun.com/debian-security buster/updates main\n\
deb-src http://mirrors.aliyun.com/debian-security buster/updates main\n\
deb http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib\n\
deb-src http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib\n\
deb http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib\n\
deb-src http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib" > /etc/apt/sources.list && \
echo  "[global]\n\
trusted-host=mirrors.aliyun.com\n\
index-url=http://mirrors.aliyun.com/pypi/simple" > /etc/pip.conf && \
ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone


#安装 mysqlclient tushare (pandas ,numpy)
# apt-get autoremove -y 删除没有用的依赖lib。减少镜像大小。1MB 也要节省。
# apt-get --purge remove 软件包名称 , 删除已安装包（不保留配置文件)。
RUN apt-get update && \
    apt-get install -y gcc make axel default-libmysqlclient-dev libxml2-dev cron && \
    pip3 install mysqlclient sqlalchemy && \
    pip3 install numpy pandas  && \
    pip3 install tushare && \
    apt-get --purge remove -y gcc make axel python3-dev default-libmysqlclient-dev libxml2-dev && \
    rm -rf /root/.cache/* && apt-get clean && apt-get autoremove -y

# pip3 install requests && \
# pip3 install lxml bs4 && \
# apt-get install -y gcc make axel python3-dev default-libmysqlclient-dev libxml2-dev cron supervisor && \
# apt-get --purge remove -y gcc make axel python3-dev default-libmysqlclient-dev libxml2-dev && \

# /usr/local/lib/python3.6/site-packages/pandas/
# 1.解决 pandas 数据插入问题。直接修改数据库驱动 sqlalchemy
# 修改：statement.replace("INSERT INTO","INSERT IGNORE INTO")
# /usr/local/lib/python3.6/site-packages/sqlalchemy/dialects/mysql/mysqldb.py
# 增加了一个 IGNORE 参数。
# 2.解决torndb在python3下面的问题：
# http://blog.csdn.net/littlethunder/article/details/8917378
# 3. 解决 type 问题，使用sed 进行替换。
#  File "/usr/local/lib/python3.6/site-packages/torndb.py", line 260, in <module>
#    CONVERSIONS[field_type] = [(FLAG.BINARY, str)] + CONVERSIONS[field_type]
#  TypeError: can only concatenate list (not "type") to list

RUN echo `date +%Y-%m-%d:%H:%M:%S` >> /etc/docker.build && \
    rm -f /etc/cron.daily/apt-compat /etc/cron.daily/dpkg /etc/cron.daily/passwd

# sed -i -e 's/executemany(statement/executemany(statement.replace\("INSERT INTO","INSERT IGNORE INTO")/g' \
#     /usr/local/lib/python3.6/site-packages/sqlalchemy/dialects/mysql/mysqldb.py && \
#    sed -i -e 's/itertools\.izip/zip/g' \
#    /usr/local/lib/python3.6/site-packages/torndb.py  && \
#    sed -i -e 's/\+ CONVERSIONS\[field_type\]/\+ \[CONVERSIONS\[field_type\],bytes\]/g' \
#    /usr/local/lib/python3.6/site-packages/torndb.py

#增加语言utf-8
ENV LANG=zh_CN.UTF-8
ENV LC_CTYPE=zh_CN.UTF-8
ENV LC_ALL=C
ENV PYTHONPATH=/data

#RUN pip3 install sklearn xlrd && apt-get install -y procps vim &&
#    echo "set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936" >> /etc/vim/vimrc && \
#    echo "set termencoding=utf-8" >> /etc/vim/vimrc && \
#    echo "set encoding=utf-8" >> /etc/vim/vimrc && apt-get clean


