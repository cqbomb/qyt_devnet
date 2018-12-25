#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import pg8000
from datetime import datetime
from qyt_devnet_0_DB_login import psql_ip, psql_username, psql_password, psql_db_name


def lifetime_netflow():
    # 连接数据库
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    # 查询数据库qytdb_lifetimenetflow,获取netflow信息的老化时间
    cursor.execute("SELECT * FROM qytdb_lifetimenetflow")
    result = cursor.fetchall()
    if len(result) == 0:  # 如果没有设置老化时间, 写入默认值24小时
        cursor.execute("insert into qytdb_lifetimenetflow values (1, 24)")
        conn.commit()
        lifetime_hours = 24  # 返回老化时间为24小时
    else:
        lifetime_hours = result[0][1]  # 如果存在设置的老化时间, 返回设置的值

    # 删除超过老化时间的netflow信息
    sqlcmd = "DELETE FROM qytdb_netflow where date < CURRENT_TIMESTAMP - INTERVAL '" + str(lifetime_hours) + " hours'"
    cursor.execute(sqlcmd)
    conn.commit()


if __name__ == "__main__":
    lifetime_netflow()


