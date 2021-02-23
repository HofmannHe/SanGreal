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

RUN echo `date +%Y-%m-%d:%H:%M:%S` >> /etc/docker.build && \
    rm -f /etc/cron.daily/apt-compat /etc/cron.daily/dpkg /etc/cron.daily/passwd

#增加语言utf-8
ENV LANG=zh_CN.UTF-8
ENV LC_CTYPE=zh_CN.UTF-8
ENV LC_ALL=C
ENV PYTHONPATH=/data
