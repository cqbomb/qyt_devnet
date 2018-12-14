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

psql_ip = "192.168.1.11"
psql_username = "qytangdbuser"
psql_password = "Cisc0123"
psql_db_name = "qytangdb"


def interfaces_speed(now, min_before):
    current_speed = (now - min_before) * 8 / 60
    return current_speed


def interfaces_utilization(ifs_speeds_list, ifs_bw_list):
    interfaces_utilization_list = []
    for x in zip(ifs_speeds_list, ifs_bw_list):
        interfaces_utilization_list.append((x[0][0], x[0][1]/int(x[1][1])))
    return interfaces_utilization_list


def max_utilization_def(old_max, current):
    return_max_utilization = []
    for x in zip(old_max, current):
        if x[1][1] > x[0][1]:
            return_max_utilization.append((x[0][0], x[1][1]))
        else:
            return_max_utilization.append((x[0][0], x[0][1]))
    return return_max_utilization



def update_deviceinterfaces_utilization():
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    sqlcmd = "SELECT name as devicename,COUNT(*) as num from qytdb_devicestatus where date >  CURRENT_TIMESTAMP - INTERVAL '119 seconds' group by name"
    cursor.execute(sqlcmd)
    device_result = cursor.fetchall()

    device_list = []
    for device in device_result:
        if device[1] == 2:
            device_list.append(device[0])

    for device in device_list:
        sqlcmd = "SELECT interfaces_rx, interfaces_tx from qytdb_devicestatus where date >  CURRENT_TIMESTAMP - INTERVAL '119 seconds' and name = '" + device + "'"
        cursor.execute(sqlcmd)
        bytes_result = cursor.fetchall()
        # print(bytes_result)
        # print(device)
        # print("1_min_before_rx")
        # print(json.loads(bytes_result[0][0]))
        # print("now_rx")
        # print(json.loads(bytes_result[1][0]))
        # print("1_min_before_tx")
        # print(json.loads(bytes_result[0][1]))
        # print("now_tx")
        # print(json.loads(bytes_result[1][1]))

        speed_list_rx = []
        for x in zip(json.loads(bytes_result[0][0]), json.loads(bytes_result[1][0])):
            # print(x)
            speed_list_rx.append((x[0][0], interfaces_speed(int(x[1][1]), int(x[0][1]))))
        print(speed_list_rx)

        speed_list_tx = []
        for x in zip(json.loads(bytes_result[0][1]), json.loads(bytes_result[1][1])):
            # print(x)
            speed_list_tx.append((x[0][0], interfaces_speed(int(x[1][1]), int(x[0][1]))))
        print(speed_list_tx)

        sqlcmd = "SELECT interfaces_bw from qytdb_deviceinterfaces where name = '" + device + "'"
        cursor.execute(sqlcmd)
        interfaces_bw_result = cursor.fetchall()
        interfaces_bw = json.loads(interfaces_bw_result[0][0])
        interfaces_utilization_rx_list = interfaces_utilization(speed_list_rx, interfaces_bw)
        # print(interfaces_utilization_rx_list)
        interfaces_utilization_tx_list = interfaces_utilization(speed_list_tx, interfaces_bw)
        # print(interfaces_utilization_tx_list)

        sqlcmd = "SELECT interfaces_max_utilization_rx, interfaces_max_utilization_tx from qytdb_deviceinterfaces_utilization where name = '" + device + "' and id = (SELECT max(id) FROM qytdb_deviceinterfaces_utilization where name = '" + device + "')"
        cursor.execute(sqlcmd)
        max_utilization = cursor.fetchall()
        try:
            max_utilization_rx = max_utilization[0][0]
        except IndexError:
            max_utilization_rx = False
        try:
            max_utilization_tx = max_utilization[0][1]
        except IndexError:
            max_utilization_tx = False

        if max_utilization_rx:
            max_utilization_rx = max_utilization_def(json.loads(max_utilization_rx), interfaces_utilization_rx_list)

        else:
            max_utilization_rx = interfaces_utilization_rx_list

        if max_utilization_tx:
            max_utilization_tx = max_utilization_def(json.loads(max_utilization_tx), interfaces_utilization_tx_list)

        else:
            max_utilization_tx = interfaces_utilization_tx_list

        sqlcmd = "insert into qytdb_deviceinterfaces_utilization (name, interfaces_bw, interfaces_max_utilization_rx, interfaces_current_speed_rx, interfaces_current_utilization_rx, interfaces_max_utilization_tx, interfaces_current_speed_tx, interfaces_current_utilization_tx, date) values ('" + device + "', '" + json.dumps(interfaces_bw) + "', '" + json.dumps(max_utilization_rx) + "', '" + json.dumps(speed_list_rx) + "', '" + json.dumps(interfaces_utilization_rx_list) + "', '" + json.dumps(max_utilization_tx) + "', '" + json.dumps(speed_list_tx) + "', '" + json.dumps(interfaces_utilization_tx_list) + "', '" + str(datetime.now()) +"')"
        # print(sqlcmd)
        cursor.execute(sqlcmd)
        conn.commit()


if __name__ == '__main__':
    update_deviceinterfaces_utilization()
