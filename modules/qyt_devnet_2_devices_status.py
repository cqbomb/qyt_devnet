#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
import pg8000
from qyt_devnet_0_snmp_get import get_mem_cpu
from qyt_devnet_0_snmp_getnext import get_ifs
import json
from datetime import datetime
psql_ip = "192.168.1.11"
psql_username = "qytangdbuser"
psql_password = "Cisc0123"
psql_db_name = "qytangdb"


def get_devices_status():
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    cursor.execute("select ip, type, name, snmp_ro_community from qytdb_devicedb")
    result = cursor.fetchall()
    for device in result:
        device_name = device[2]
        cursor.execute("select snmp_reachable from qytdb_device_reachable where name = '" + device_name + "'")
        result = cursor.fetchall()
        if result[0][0] == True:
            device_mem_cpu = get_mem_cpu(str(device[0]), device[1], device[3])
            device_ifs_info = get_ifs(str(device[0]), device[1], device[3])
            device_mem = device_mem_cpu[0]
            device_cpu = device_mem_cpu[1]
            # print(device_ifs_info)
            device_ifs_num = len(device_ifs_info)
            # print(device_ifs_num)
            device_ifs_interfaces = json.dumps([ x[0] for x in device_ifs_info ])
            # print(device_ifs_interfaces)
            device_ifs_interfaces_bw = json.dumps([ {x[0]: x[1]} for x in device_ifs_info ])
            # print(device_ifs_interfaces_bw)
            device_ifs_interfaces_rx = json.dumps([ {x[0]: x[2]} for x in device_ifs_info ])
            # print(device_ifs_interfaces_rx)
            device_ifs_interfaces_tx = json.dumps([ {x[0]: x[3]} for x in device_ifs_info ])
            # print(device_ifs_interfaces_tx)
            # print(device_mem)
            # print(device_cpu)
            sqlcmd = "INSERT INTO qytdb_devicestatus (name, interfaces, interfaces_rx, interfaces_tx, cpu, mem, date) VALUES ('" + device_name + "', '" + device_ifs_interfaces + "', '" + device_ifs_interfaces_rx  + "', '" + device_ifs_interfaces_tx + "', " + str(device_cpu) + ", " + str(device_mem) + ", '" + str(datetime.now()) +"')"
            # print(sqlcmd)
            cursor.execute(sqlcmd)
            conn.commit()
            cursor.execute("select * from qytdb_devicecpumem where name = '" + device_name + "'")
            result = cursor.fetchall()
            cpu_max_utilization = result[0][2]
            mem_max_utilization = result[0][4]
            if device_cpu > cpu_max_utilization:
                cpu_max_utilization = device_cpu
            if device_mem > mem_max_utilization:
                mem_max_utilization = device_mem


            sqlcmd = "UPDATE qytdb_devicecpumem SET cpu_max_utilization = " + str(cpu_max_utilization) + ", mem_max_utilization = " + str(mem_max_utilization) + ", cpu_current_utilization = " + str(device_cpu) +  ", mem_current_utilization = " + str(device_mem) + " where name = '" + str(device_name) + "'"
            # print(sqlcmd)
            cursor.execute(sqlcmd)
            conn.commit()

        else:
            continue
    # sqlcmd = "SELECT * from qytdb_devicestatus where date >  CURRENT_TIMESTAMP - INTERVAL '1000 seconds' and name = 'ASA'"
    # cursor.execute(sqlcmd)
    # result = cursor.fetchall()
    # print(json.loads(result[0][3])[1]['Inside'])


if __name__ == '__main__':
    get_devices_status()
