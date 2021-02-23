FROM docker.io/python:3.8-slim-buster

WORKDIR /data

#增加语言utf-8
ENV LANG=zh_CN.UTF-8
ENV LC_CTYPE=zh_CN.UTF-8
ENV LC_ALL=C
ENV PYTHONPATH=/data

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

#add cron sesrvice.
#每分钟，每小时1分钟，每天1点1分，每月1号执行
RUN echo `date +%Y-%m-%d:%H:%M:%S` >> /etc/docker.build && \
    rm -f /etc/cron.daily/apt-compat /etc/cron.daily/dpkg /etc/cron.daily/passwd && \
    mkdir -p /etc/cron.minutely && mkdir -p /etc/cron.hourly && mkdir -p /etc/cron.monthly && \
    echo "SHELL=/bin/sh \n\
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin \n\
# min   hour    day     month   weekday command \n\
*/1     *       *       *       *       /bin/run-parts /etc/cron.minutely \n\
10       *       *       *       *       /bin/run-parts /etc/cron.hourly \n\
30       16       *       *       *       /bin/run-parts /etc/cron.daily \n\
30       17       1,10,20       *       *       /bin/run-parts /etc/cron.monthly \n" > /var/spool/cron/crontabs/root && \
    chmod 600 /var/spool/cron/crontabs/root

ADD jobs /data/jobs

ADD jobs/cron.minutely /etc/cron.minutely
ADD jobs/cron.hourly /etc/cron.hourly
ADD jobs/cron.daily /etc/cron.daily
ADD jobs/cron.monthly /etc/cron.monthly

RUN mkdir -p /data/logs && ls /data/stock/ && chmod 755 /data/stock/jobs/run_* &&  \
    chmod 755 /etc/cron.minutely/* && chmod 755 /etc/cron.hourly/* && \
    chmod 755 /etc/cron.daily/* && chmod 755 /etc/cron.monthly/*

ENTRYPOINT ["supervisord","-n","-c","/data/supervisor/supervisord.conf"]