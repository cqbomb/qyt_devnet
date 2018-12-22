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
    # 查询数据库qytdb_devicedb,获取ip, type, name, snmp_ro_community, ssh_username, ssh_password, enable_password等信息
    cursor.execute("SELECT * FROM qytdb_lifetimedevicestatus")
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.execute("insert into qytdb_lifetimedevicestatus values (1, 'devicestatuslifetime', 24)")
        conn.commit()
        lifetime_hours = 24
    else:
        lifetime_hours = result[0][2]

    sqlcmd = "DELETE FROM qytdb_devicestatus where date < CURRENT_TIMESTAMP - INTERVAL '" + str(lifetime_hours) + " hours'"
    cursor.execute(sqlcmd)
    conn.commit()


if __name__ == "__main__":
    lifetime_netflow()


