#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import pg8000
import json
from datetime import datetime
import time
psql_ip = "192.168.1.11"
psql_username = "qytangdbuser"
psql_password = "Cisc0123"
psql_db_name = "qytangdb"

conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
cursor = conn.cursor()
sqlcmd = "SELECT interfaces_current_speed_rx, interfaces_current_speed_tx , interfaces_max_utilization_rx, interfaces_max_utilization_tx from qytdb_deviceinterfaces_utilization where name = 'ASA' and id = (SELECT max(id) FROM qytdb_deviceinterfaces_utilization where name = 'ASA')"

while True:
    cursor.execute(sqlcmd)
    device_result = cursor.fetchall()
    print(json.loads(device_result[0][0]))
    print(json.loads(device_result[0][1]))
    print(json.loads(device_result[0][2]))
    print(json.loads(device_result[0][3]))
    print('-'* 80)
    time.sleep(5)
