#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
import pg8000
import json
from qyt_devnet_0_snmp_get import get_mem_cpu
from qyt_devnet_0_snmp_getnext import get_ifs
from datetime import datetime, timezone, timedelta
from qyt_devnet_0_DB_login import psql_ip, psql_username, psql_password, psql_db_name
from qyt_devnet_0_smtp import qyt_smtp_attachment


# 用于获取数据库中设置的CPU告警阈值,告警周期,与上一次告警的时间.并且判断时间超出告警周期后返回结果.
def get_threshold_cpu():
    # 连接PSQL数据库
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    # 设置时区为东八区
    tzutc_8 = timezone(timedelta(hours=8))
    # 获取表qytdb_thresholdcpu中的cpu_threshold, alarm_interval, last_alarm_time信息,只有一个条目所有id=1
    cursor.execute("select cpu_threshold, alarm_interval, last_alarm_time from qytdb_thresholdcpu where id=1")
    result = cursor.fetchall()
    try:
        # 计算当前时间与上一次告警时间的增量,如果无法获取上一次告警时间就返回None(客户没有设置告警阈值,只要设置了自动会设置上一次告警时间为当前时间)
        delta_time = datetime.now().replace(tzinfo=tzutc_8) - result[0][2]
    except Exception:
        return None
    # 判断增量时间的秒数是否大于告警周期, 如果大于就返回CPU告警阈值,否则返回None
    if delta_time.seconds > result[0][1]*60:
        return result[0][0]
    else:
        return None


# 用于获取数据库中设置的内存告警阈值,告警周期,与上一次告警的时间.并且判断时间超出告警周期后返回结果.
def get_threshold_mem():
    # 连接PSQL数据库
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    tzutc_8 = timezone(timedelta(hours=8))
    # 获取表qytdb_thresholdmem中的mem_threshold, alarm_interval, last_alarm_time信息,只有一个条目所有id=1
    cursor.execute("select mem_threshold, alarm_interval, last_alarm_time from qytdb_thresholdmem where id=1")
    result = cursor.fetchall()
    try:
        # 计算当前时间与上一次告警时间的增量,如果无法获取上一次告警时间就返回None(客户没有设置告警阈值,只要设置了自动会设置上一次告警时间为当前时间)
        delta_time = datetime.now().replace(tzinfo=tzutc_8) - result[0][2]
    except Exception:
        return None
    # 判断增量时间的秒数是否大于告警周期, 如果大于就返回内存告警阈值,否则返回None
    if delta_time.seconds > result[0][1]*60:
        return result[0][0]
    else:
        return None


# 获取smtp服务器与登录信息
def get_mail_login():
    # 连接PSQL数据库
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    # 获取表qytdb_smtplogindb中的smtp服务器与登录信息
    cursor.execute("select mailserver, mailusername, mailpassword, mailfrom, mailto from qytdb_smtplogindb where id=1")
    result = cursor.fetchall()
    if result:
        # 如果客户设置了smtp服务器与登录信息就返回,如果没有就返回None
        return result[0]
    else:
        return None


def get_devices_status():
    # mail_send参数用于记录告警邮件是否被发送,默认设置为False(未发送)
    cpu_mail_send = False
    mem_mail_send = False
    # 获取CPU阈值信息,如果客户未设置,或者时间未超出告警周期就返回None
    cpu_threshold = get_threshold_cpu()
    # 获取内存阈值信息,如果客户未设置,或者时间未超出告警周期就返回None
    mem_threshold = get_threshold_mem()
    # 获取smtp服务器与登录信息,如果客户未设置就返回None
    mail_login_info = get_mail_login()
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
            # 数据分别为: 接口名字, 物理带宽, 入向字节数, 出向字节数
            device_ifs_info = get_ifs(str(device[0]), device[1], device[3])
            # 获取内存利用率
            device_mem = device_mem_cpu[0]
            if mem_threshold and mail_login_info:  # 如果内存告警阈值和SMTP信息都存在
                if device_mem > mem_threshold:  # 如果当前内存利用率高于内存告警阈值
                    # 发送告警邮件, 将会书写主题(包含设备名)和正文(包含设备名与当前内存利用率)
                    qyt_smtp_attachment(mail_login_info[0], mail_login_info[1], mail_login_info[2], mail_login_info[3], mail_login_info[4], device_name + " MEM警告", device_name + "当前MEM利用率为 " + str(device_mem) + "%")
                    # 将已发送邮件设置为True
                    mem_mail_send = True
            # 获取CPU利用率
            device_cpu = device_mem_cpu[1]
            if cpu_threshold and mail_login_info:  # 如果CPU告警阈值和SMTP信息都存在
                if device_cpu > cpu_threshold:  # 如果当前CPU利用率高于CPU告警阈值
                    # 发送告警邮件, 将会书写主题(包含设备名)和正文(包含设备名与当前CPU利用率)
                    qyt_smtp_attachment(mail_login_info[0], mail_login_info[1], mail_login_info[2], mail_login_info[3], mail_login_info[4], device_name + " CPU警告", device_name + "当前CPU利用率为 " + str(device_cpu) + "%")
                    # 将已发送邮件设置为True
                    cpu_mail_send = True
            # 通过计算device_ifs_info列表的长度来计算接口数量
            device_ifs_num = len(device_ifs_info)
            # 接口名称列表 ["Ethernet0/0", "Ethernet0/1", "Ethernet0/2"]
            device_ifs_interfaces = json.dumps([x[0] for x in device_ifs_info])
            # 接口物理带宽列表 [["Ethernet0/0", "10000"], ["Ethernet0/1", "10000"], ["Ethernet0/2", "10000"]]
            # 注意带宽单位为kbps
            device_ifs_interfaces_bw = json.dumps([(x[0], int(x[1])/1000) for x in device_ifs_info])
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

    if cpu_mail_send:  # 如果CPU告警邮件已经发送
        time_now = str(datetime.now())  # 获取当前时间
        # 设置当前时间到CPU告警的上一次告警时间
        sqlcmd = "UPDATE qytdb_thresholdcpu SET last_alarm_time = '" + time_now + "' where id = 1"
        cursor.execute(sqlcmd)
        conn.commit()

    if mem_mail_send:  # 如果内存告警邮件已经发送
        time_now = str(datetime.now())  # 获取当前时间
        # 设置当前时间到内存告警的上一次告警时间
        sqlcmd = "UPDATE qytdb_thresholdmem SET last_alarm_time = '" + time_now + "' where id = 1"
        cursor.execute(sqlcmd)
        conn.commit()


if __name__ == '__main__':
    get_devices_status()
