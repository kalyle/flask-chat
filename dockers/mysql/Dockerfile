
FROM mysql:8.0.23

ENV MYSQL_ROOT_PASSWORD 123456

# 将相对于Dockefile位置的脚本添加到镜像中
COPY start.sh /start.sh

EXPOSE 3307
# 将初始化SQL脚本复制到镜像中
# COPY init.sql /docker-entrypoint-initdb.d/
VOLUME ["/etc/my.cnf","/var/lib/mysql"]

 
CMD ["sh","start.sh"]
