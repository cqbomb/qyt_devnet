#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from django.shortcuts import render
from qytdb.models import Netflow
import pg8000
from django.http import JsonResponse

psql_ip = "192.168.1.11"
psql_username = "qytangdbuser"
psql_password = "Cisc0123"
psql_db_name = "qytangdb"

protocol_map = {'6/22': 'SSH',
                '6/23': 'Telnet',
                '17/137': 'UDP NETBIOS Name Service',
                '17/138': 'UDP NETBIOS Datagram Service',
                '17/5353': 'MDNS',
                '17/53': 'DNS',
                '6/80': 'HTTP',
                '6/443': 'HTTPS',
                '17/5355': 'LLMNR'}


def netflow_show(request):
    return render(request, 'netflow.html')


def netflow_protocol(request):
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    cursor.execute("select dst_port,protocol from qytdb_netflow group by dst_port, protocol")
    yourresults = cursor.fetchall()

    application_list = []

    # 找到出现的应用(协议,目的端口)
    for dbinfo in yourresults:
        application_list.append(dbinfo)

    protocol_list = []
    protocol_bytes = []
    for x in application_list:
        # 提取应用(协议,目的端口)的入向字节数
        cursor.execute("select in_bytes from qytdb_netflow where protocol='%s' and dst_port='%s'" % (x[1], x[0]))
        yourresults = cursor.fetchall()
        bytes_sum = 0
        # 把每一个会话的字节数加起来
        for dbinfo in yourresults:
            bytes_sum += dbinfo[0]
        protocol_port = str(x[1]) + '/' + str(x[0])
        # 把协议清单写入protocol_list
        protocol_list.append(protocol_map.get(protocol_port, protocol_port))
        # 把协议对于的字节数,写入protocol_bytes
        protocol_bytes.append(bytes_sum)

    if len(protocol_list) > 5:
        labels = protocol_list[:5]
        datas = protocol_bytes[:5]
    else:
        labels = protocol_list
        datas = protocol_bytes

    colors = ['#228b22', '#ffff00', '#ff0000', '#3342FF', '#524b22']
    return JsonResponse({'colors': colors, 'labels': labels, 'datas': datas})


def netflow_top_ip(request):
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    cursor.execute("select src_ip from qytdb_netflow group by src_ip")
    yourresults = cursor.fetchall()

    ip_list = []

    # 找到出现的应用(协议,目的端口)
    for dbinfo in yourresults:
        ip_list.append(dbinfo)


    bytes_list = []
    for x in ip_list:
        # 提取应用(协议,目的端口)的入向字节数
        sqlcmd = "select in_bytes from qytdb_netflow where src_ip='" + x[0] + "'"
        print(sqlcmd)
        cursor.execute(sqlcmd)
        yourresults = cursor.fetchall()
        bytes_sum = 0
        # 把每一个会话的字节数加起来
        for dbinfo in yourresults:
            bytes_sum += dbinfo[0]
    #
    #     ip_list.append(protocol_map.get(protocol_port, protocol_port))
    #     # 把协议对于的字节数,写入protocol_bytes
        bytes_list.append(bytes_sum)
    #
    if len(ip_list) > 5:
        labels = ip_list[:5]
        datas = bytes_list[:5]
    else:
        labels = ip_list
        datas = bytes_list
    #
    colors = ['#228b22', '#ffff00', '#ff0000', '#3342FF', '#524b22']
    return JsonResponse({'colors': colors, 'labels': labels, 'datas': datas})

