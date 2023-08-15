
FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD root

# 将相对于Dockefile位置的脚本添加到镜像中
COPY start.sh /start.sh
# 和 -P效果相同，随机映射主机端口，如果docker run指定 -p 则默认 -p 
EXPOSE 3306

# 将初始化SQL脚本复制到镜像中
# COPY init.sql /docker-entrypoint-initdb.d/

# -v "~/funchat/mysql/data:/var/lib/mysql" -v "~/funchat/mysql/my.cnf:/etc/my.cnf"
 
ENTRYPOINT ["sh","start.sh"]
