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
    # 连接PSQL数据库
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    # 获取表qytdb_devicedb中的ip, type, name, snmp_ro_community信息
    cursor.execute("select ip, type, name, snmp_ro_community from qytdb_devicedb")
    result = cursor.fetchall()
    for device in result:
        # 提取设备名 device[2]
        device_name = device[2]
        # 查询设备的SNMP可达性信息
        cursor.execute("select snmp_reachable from qytdb_device_reachable where name = '" + device_name + "'")
        result = cursor.fetchall()
        # 如果SNMP可达
        if result[0][0]:
            # 获取设备的内存和CPU利用率,(50, 38)前为内存利用率,后为CPU利用率
            device_mem_cpu = get_mem_cpu(str(device[0]), device[1], device[3])
            # 获取设备的接口信息, [('Ethernet0/0', '10000000', '68743319', '61244177'), ('Ethernet0/1', '10000000', '42188070', '884326731'), ('Ethernet0/2', '10000000', '866143457', '61391685')]
            device_ifs_info = get_ifs(str(device[0]), device[1], device[3])
            # 获取内存利用率
            device_mem = device_mem_cpu[0]
            # 获取CPU利用率
            device_cpu = device_mem_cpu[1]
            # 通过计算device_ifs_info列表的长度来计算接口数量
            device_ifs_num = len(device_ifs_info)
            # 接口名称列表 ["Ethernet0/0", "Ethernet0/1", "Ethernet0/2"]
            device_ifs_interfaces = json.dumps([x[0] for x in device_ifs_info ])
            # 接口物理带宽列表 [["Ethernet0/0", "10000000"], ["Ethernet0/1", "10000000"], ["Ethernet0/2", "10000000"]]
            device_ifs_interfaces_bw = json.dumps([(x[0], int(x[1])) for x in device_ifs_info])
            # 接口入向字节数列表 [["Ethernet0/0", "68847030"], ["Ethernet0/1", "42267283"], ["Ethernet0/2", "866265171"]]
            device_ifs_interfaces_rx = json.dumps([(x[0], int(x[2])) for x in device_ifs_info])
            # 接口出向字节数列表 [["Ethernet0/0", "61360003"], ["Ethernet0/1", "884452854"], ["Ethernet0/2", "61475786"]]
            device_ifs_interfaces_tx = json.dumps([(x[0], int(x[3])) for x in device_ifs_info])

            # 插入name, interfaces, interfaces_rx, interfaces_tx, cpu, mem, date信息到表qytdb_devicestatus
            sqlcmd = "INSERT INTO qytdb_devicestatus (name, interfaces, interfaces_rx, interfaces_tx, cpu, mem, date) VALUES ('" + device_name + "', '" + device_ifs_interfaces + "', '" + device_ifs_interfaces_rx  + "', '" + device_ifs_interfaces_tx + "', " + str(device_cpu) + ", " + str(device_mem) + ", '" + str(datetime.now()) + "')"
            cursor.execute(sqlcmd)
            conn.commit()
            # 查询qytdb_devicecpumem中曾今记录的最大内存和CPU利用率
            cursor.execute("select * from qytdb_devicecpumem where name = '" + device_name + "'")
            result = cursor.fetchall()
            # 曾今记录的最大CPU利用率
            cpu_max_utilization = result[0][2]
            # 曾今记录的最大内存利用率
            mem_max_utilization = result[0][4]
            # 如果当前CPU利用率高于,历史曾经记录的最大CPU利用率
            if device_cpu > cpu_max_utilization:
                # 使用当前CPU利用率,刷新历史曾经记录的最大CPU利用率
                cpu_max_utilization = device_cpu
            # 如果当前内存利用率高于,历史曾经记录的最大内存利用率
            if device_mem > mem_max_utilization:
                # 使用当前内存利用率,刷新历史曾经记录的最大内存利用率
                mem_max_utilization = device_mem
            # 更新qytdb_devicecpumem表中的记录,这个表不随着时间的增加而添加额外的项目,仅仅记录状态
            sqlcmd = "UPDATE qytdb_devicecpumem SET cpu_max_utilization = " + str(cpu_max_utilization) + ", mem_max_utilization = " + str(mem_max_utilization) + ", cpu_current_utilization = " + str(device_cpu) + ", mem_current_utilization = " + str(device_mem) + " where name = '" + str(device_name) + "'"
            cursor.execute(sqlcmd)
            conn.commit()
            # 更新qytdb_deviceinterfaces表中的记录,这个表不随着时间的增加而添加额外的项目,仅仅记录状态
            sqlcmd = "UPDATE qytdb_deviceinterfaces SET interfaces_num = " + str(device_ifs_num) + ", interfaces = '" + device_ifs_interfaces + "', interfaces_bw = '" + device_ifs_interfaces_bw + "' where name = '" + str(device_name) + "'"
            cursor.execute(sqlcmd)
            conn.commit()

        else:
            continue


if __name__ == '__main__':
    get_devices_status()
