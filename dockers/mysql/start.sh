#/bin/bash

# MySQL登录信息
mysql_user="root"
mysql_password="$MYSQL_ROOT_PASSWORD"

# 执行MySQL登录命令
mysql  -u $mysql_user -p$mysql_password

echo "连接成功"