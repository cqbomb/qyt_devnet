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
from qyt_devnet_0_DB_login import psql_ip, psql_username, psql_password, psql_db_name
from datetime import timezone, timedelta
from qyt_devnet_0_smtp import qyt_smtp_attachment

# /etc/crontab 调度设置
# *  *  *  *  * root /usr/local/bin/python3 /devnet/modules/qyt_devnet_3_interfaces_utilization.py


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


# 用于获取数据库中设置的接口利用率告警阈值,告警周期,与上一次告警的时间.并且判断时间超出告警周期后返回结果.
def get_threshold_utilization():
    # 连接PSQL数据库
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    # 设置时区为东八区
    tzutc_8 = timezone(timedelta(hours=8))
    # 获取表qytdb_thresholdutilization中的utilization_threshold, alarm_interval, last_alarm_time信息,只有一个条目所有id=1
    cursor.execute("select utilization_threshold, alarm_interval, last_alarm_time from qytdb_thresholdutilization where id=1")
    result = cursor.fetchall()
    try:
        # 计算当前时间与上一次告警时间的增量,如果无法获取上一次告警时间就返回None(客户没有设置告警阈值,只要设置了自动会设置上一次告警时间为当前时间)
        delta_time = datetime.now().replace(tzinfo=tzutc_8) - result[0][2]
    except Exception:
        return None
    # 判断增量时间的秒数是否大于告警周期, 如果大于就返回接口利用率告警阈值,否则返回None
    if delta_time.seconds > result[0][1]*60:
        return result[0][0]
    else:
        return None


# 通过计算当前字节数,与一分钟前字节数的增量来计算接口速率
def interfaces_speed(now, min_before, time_now, time_before):
    # * 8 是因为采集的是字节,计算速率的时候单位为bit
    # / 60 是因为采集周期为分钟,这个与后台调度程序crond的调度有关
    # / 1000 是因为要保持速率单位为kbps,与带宽的单位保持一致,便于后续利用率的计算
    # round(x, 2)表示控制浮点数的精度为小数点后两位
    current_speed = round((((now - min_before) * 8 / (time_now - time_before).seconds) / 1000), 2)
    return current_speed


# 计算接口利用率
def interfaces_utilization(name, dirct, utilization_threshold, mail_login_info, ifs_speeds_list, ifs_bw_list):
    # mail_send参数用于记录告警邮件是否被发送,默认设置为False(未发送)
    mail_send = False
    interfaces_utilization_list = []
    for x in zip(ifs_speeds_list, ifs_bw_list):  # 把速率与带宽 压(zip)到一起
        # 计算接口利用率 速率(kbps)/带宽(kbps)
        # * 100 是让利用率的单位为 %
        # round(x, 2)表示控制浮点数的精度为小数点后两位
        interfaces_utilization_percent = round((x[0][1]/x[1][1]) * 100, 2)
        if mail_login_info and utilization_threshold:  # 如果接口利用率告警阈值和SMTP信息都存在
            if interfaces_utilization_percent >= utilization_threshold:  # 如果当前接口利用率高于告警阈值
                # 发送告警邮件, 将会书写主题(包含设备名, 接口和方向)和正文(包含设备名, 接口, 方向和当前利用率)
                qyt_smtp_attachment(mail_login_info[0], mail_login_info[1], mail_login_info[2], mail_login_info[3],
                                    mail_login_info[4], name + " 接口 " + x[0][0] + " " + dirct + " 方向利用率警告",
                                    name + " 接口 " + x[0][0] + " " + dirct + " 方向当前利用率为 " + str(interfaces_utilization_percent) + "%")
                # 将已发送邮件设置为True
                mail_send = True
        if interfaces_utilization_percent > 100:  # 过滤掉不合理的利用率,Nexus交换机容易出现这个bug
            interfaces_utilization_percent = 0

        # 接口利用率清单中包括(接口名, 接口利用率)
        interfaces_utilization_list.append((x[0][0], interfaces_utilization_percent))
    # 返回接口利用率清单和发送告警邮件状态
    return interfaces_utilization_list, mail_send


# 判断当前利用率是否超过历史最大利用率,如果超过就替换
def max_utilization_def(old_max, current):
    return_max_utilization = []
    for x in zip(old_max, current):
        if x[1][1] > x[0][1]:  # 如果当前利用率超过历史最大利用率,使用当前利用率替换,历史最大利用率
            return_max_utilization.append((x[0][0], x[1][1]))
        else:  # 如果当前利用率未能超过历史最大利用率,保持历史最大利用率
            return_max_utilization.append((x[0][0], x[0][1]))
    # 返回接口最大利用率的清单
    return return_max_utilization


# 用于更新接口利用率数据库
def update_deviceinterfaces_utilization():
    # mail_send参数用于记录告警邮件是否被发送,默认设置为False(未发送)
    mail_send = False
    # 获取接口利用率阈值信息,如果客户未设置,或者时间未超出告警周期就返回None
    utilization_threshold = get_threshold_utilization()
    # 获取smtp服务器与登录信息,如果客户未设置就返回None
    mail_login_info = get_mail_login()
    # 连接数据库
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    # 搜索最近两分钟(where date >  CURRENT_TIMESTAMP - INTERVAL '119 seconds')特定设备在表qytdb_devicestatus中的记录数量
    sqlcmd = "SELECT name as devicename,COUNT(*) as num from qytdb_devicestatus where date >  CURRENT_TIMESTAMP - INTERVAL '119 seconds' group by name"
    cursor.execute(sqlcmd)
    device_result = cursor.fetchall()

    device_list = []
    for device in device_result:
        # 如果记录数为2,表示正常被记录的设备
        if device[1] == 2:
            # 把设备名,添加到待查询的设备清单
            device_list.append(device[0])

    for device in device_list:
        #  查询最近两分钟(where date >  CURRENT_TIMESTAMP - INTERVAL '119 seconds')特定设备的两条记录(之前判断过)
        sqlcmd = "SELECT interfaces_rx, interfaces_tx, date from qytdb_devicestatus where date >  CURRENT_TIMESTAMP - INTERVAL '119 seconds' and name = '" + device + "'"
        cursor.execute(sqlcmd)
        bytes_result = cursor.fetchall()
        # print(bytes_result)
        # # (['[["Outside", "739590134"], ["Inside", "36253690"], ["MGMT", "59582884"]]', '[["Outside", "32375277"], ["Inside", "738191427"], ["MGMT", "75374210"]]'], ['[["Outside", "739596374"], ["Inside", "36263389"], ["MGMT", "59619623"]]', '[["Outside", "32384615"], ["Inside", "738196871"], ["MGMT", "75422155"]]'])
        # print(device)
        # print("1_min_before_rx")
        # print(json.loads(bytes_result[0][0]))
        # # [['Outside', '739590134'], ['Inside', '36253690'], ['MGMT', '59582884']]
        # print("now_rx")
        # print(json.loads(bytes_result[1][0]))
        # # [['Outside', '739596374'], ['Inside', '36263389'], ['MGMT', '59619623']]
        # print("1_min_before_tx")
        # print(json.loads(bytes_result[0][1]))
        # # [['Outside', '32375277'], ['Inside', '738191427'], ['MGMT', '75374210']]
        # print("now_tx")
        # print(json.loads(bytes_result[1][1]))
        # # [['Outside', '32384615'], ['Inside', '738196871'], ['MGMT', '75422155']]

        # 计算入方向速率列表
        speed_list_rx = []
        # bytes_result[0][0]) 为一分钟前入向字节数
        # bytes_result[1][0]) 为当前入向字节数
        # print(bytes_result[0][2])
        # print(bytes_result[1][2])
        for x in zip(json.loads(bytes_result[0][0]), json.loads(bytes_result[1][0])):
            # 产生接口入向速率清单, 使用abs依然是防止Nexus计算速率为负数的可能
            speed_list_rx.append((x[0][0], abs(interfaces_speed(x[1][1], x[0][1], bytes_result[1][2], bytes_result[0][2]))))

        # 计算出方向速率列表
        speed_list_tx = []
        # bytes_result[0][1]) 为一分钟前出向字节数
        # bytes_result[1][1]) 为当前出向字节数
        for x in zip(json.loads(bytes_result[0][1]), json.loads(bytes_result[1][1])):
            # 产生接口出向速率清单, 使用abs依然是防止Nexus计算速率为负数的可能
            speed_list_tx.append((x[0][0], abs(interfaces_speed(x[1][1], x[0][1], bytes_result[1][2], bytes_result[0][2]))))

        # 获取特定设备的物理接口带宽,用于后续计算利用率
        sqlcmd = "SELECT interfaces_bw from qytdb_deviceinterfaces where name = '" + device + "'"
        cursor.execute(sqlcmd)
        interfaces_bw_result = cursor.fetchall()
        # 得到特定设备物理接口带宽的列表
        interfaces_bw = json.loads(interfaces_bw_result[0][0])
        # 计算入向接口利用率的列表
        # 传入设备名字, 方向, 接口利用率阈值, SMTP信息主要是为了在interfaces_utilization方法的循环中发送邮件
        interfaces_utilization_rx_result = interfaces_utilization(device, 'RX', utilization_threshold, mail_login_info, speed_list_rx, interfaces_bw)

        # [0]号位置为入向接口利用率清单
        interfaces_utilization_rx_list = interfaces_utilization_rx_result[0]

        # [1]号位置为mail_send的状态,注意此处一定要判断, 否则后续接口的False会把之前的True给冲刷掉
        # 此处多次教训,请注意!!!
        if interfaces_utilization_rx_result[1]:
            mail_send = True
        # 计算出向接口利用率的列表
        # 传入设备名字, 方向, 接口利用率阈值, SMTP信息主要是为了在interfaces_utilization方法的循环中发送邮件
        interfaces_utilization_tx_result = interfaces_utilization(device, 'TX', utilization_threshold, mail_login_info, speed_list_tx, interfaces_bw)

        # [0]号位置为出向接口利用率清单
        interfaces_utilization_tx_list = interfaces_utilization_tx_result[0]

        # [1]号位置为mail_send的状态,注意此处一定要判断, 否则后续接口的False会把之前的True给冲刷掉
        # 此处多次教训,请注意!!!
        if interfaces_utilization_tx_result[1]:
            mail_send = True

        # 获取最后一次(id = (SELECT max(id) FROM qytdb_deviceinterfaces_utilization where name = 'device'))记录的, 历史最大入向和出向接口利用率
        # 注意qytdb_deviceinterfaces_utilization是一个不断记录不断累加的数据库表
        sqlcmd = "SELECT interfaces_max_utilization_rx, interfaces_max_utilization_tx from qytdb_deviceinterfaces_utilization where name = '" + device + "' and id = (SELECT max(id) FROM qytdb_deviceinterfaces_utilization where name = '" + device + "')"
        cursor.execute(sqlcmd)
        max_utilization = cursor.fetchall()
        # 提取历史最大入向接口利用率
        try:
            max_utilization_rx = max_utilization[0][0]
        except IndexError:  # 可能并不存在之前记录的最大入向接口利用率
            max_utilization_rx = False
        # 提取历史最大出向接口利用率
        try:
            max_utilization_tx = max_utilization[0][1]
        except IndexError:  # 可能并不存在之前记录的最大出向接口利用率
            max_utilization_tx = False

        # 如果存在之前记录的历史最大入向接口利用率,那就与当前利用率进行比较!得到新的最大利用率
        if max_utilization_rx:
            max_utilization_rx = max_utilization_def(json.loads(max_utilization_rx), interfaces_utilization_rx_list)
        # 如果不存在之前记录的历史最大入向接口利用率,把当前利用率当做最大利用率
        else:
            max_utilization_rx = interfaces_utilization_rx_list
        # 如果存在之前记录的历史最大出向接口利用率,那就与当前利用率进行比较!得到新的最大利用率
        if max_utilization_tx:
            max_utilization_tx = max_utilization_def(json.loads(max_utilization_tx), interfaces_utilization_tx_list)
        # 如果不存在之前记录的历史最大出向接口利用率,把当前利用率当做最大利用率
        else:
            max_utilization_tx = interfaces_utilization_tx_list

        # 写入数据到表qytdb_deviceinterfaces_utilization, 这个数据库会不断累加
        sqlcmd = "insert into qytdb_deviceinterfaces_utilization (name, interfaces_bw, interfaces_max_utilization_rx, interfaces_current_speed_rx, interfaces_current_utilization_rx, interfaces_max_utilization_tx, interfaces_current_speed_tx, interfaces_current_utilization_tx, date) values ('" + device + "', '" + json.dumps(interfaces_bw) + "', '" + json.dumps(max_utilization_rx) + "', '" + json.dumps(speed_list_rx) + "', '" + json.dumps(interfaces_utilization_rx_list) + "', '" + json.dumps(max_utilization_tx) + "', '" + json.dumps(speed_list_tx) + "', '" + json.dumps(interfaces_utilization_tx_list) + "', '" + str(datetime.now()) + "')"
        # print(sqlcmd)
        cursor.execute(sqlcmd)
        conn.commit()

    if mail_send:  # 如果告警邮件已经发送
        time_now = str(datetime.now())  # 获取当前时间
        # 设置当前时间到接口利用率告警的上一次告警时间
        sqlcmd = "UPDATE qytdb_thresholdutilization SET last_alarm_time = '" + time_now + "' where id = 1"
        cursor.execute(sqlcmd)
        conn.commit()


if __name__ == '__main__':
    update_deviceinterfaces_utilization()
