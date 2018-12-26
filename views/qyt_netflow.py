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
from qytdb.models import Netflowinterval
from django.contrib.auth.decorators import login_required

# 数据库信息
psql_ip = "192.168.1.11"
psql_username = "qytangdbuser"
psql_password = "Cisc0123"
psql_db_name = "qytangdb"

# 协议映射表,可以按照自己的需求继续添加
protocol_map = {'6/22': 'SSH',
                '6/23': 'Telnet',
                '17/137': 'UDP NETBIOS Name Service',
                '17/138': 'UDP NETBIOS Datagram Service',
                '17/5353': 'MDNS',
                '17/53': 'DNS',
                '6/80': 'HTTP',
                '6/443': 'HTTPS',
                '17/5355': 'LLMNR'}


def getinterval_netflow():  # 获取Netflow监控周期的方法
    result = Netflowinterval.objects.all()  # 查询Netflowinterval数据库
    if len(result) == 0:  # 如果没有结果,写入默认值一个小时
        d1 = Netflowinterval(id=1,
                             netflow_interval=1)
        d1.save()
        interval = 1  # 返回Netflow监控周期为一个小时
    else:
        # 如果存在设置的Netflow监控周期,返回数据库中的设置值
        interval = Netflowinterval.objects.get(id=1).netflow_interval

    return interval


@login_required()
def netflow_show(request):  # 显示Netflow协议分析页面"netflow.html", 页面中的JS会获取后台JSON数据, 展示图表
    return render(request, 'netflow.html')


@login_required()
def netflow_protocol(request):  # 为Netflow协议分析的"协议分布 Top 5"返回JSON数据
    # 连接数据库
    # 后期推荐修改为Django的数据库查询方案
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    # 查询Netflow数据库, 在Netflow监控周期内的目的端口和协议信息, 找到出现的目的端口和协议的组合(应用)
    cursor.execute("select dst_port,protocol from qytdb_netflow where date > CURRENT_TIMESTAMP - INTERVAL '" + str(getinterval_netflow()) + " hours' group by dst_port, protocol")
    yourresults = cursor.fetchall()

    application_list = []

    # 找到出现的应用(协议,目的端口)
    for dbinfo in yourresults:
        application_list.append(dbinfo)

    protocol_list = []
    protocol_bytes = []
    for x in application_list:
        # 提取应用(协议,目的端口)的入向字节数
        sqlcmd = "select in_bytes from qytdb_netflow where protocol=" + str(x[1]) + " and dst_port=" + str(x[0]) + " and date > CURRENT_TIMESTAMP - INTERVAL '" + str(getinterval_netflow()) + " hours'"
        cursor.execute(sqlcmd)
        yourresults = cursor.fetchall()

        bytes_sum = 0
        # 把每一个应用的字节数加起来
        for dbinfo in yourresults:
            bytes_sum += dbinfo[0]

        # 把协议和目的端口拼接为 UDP/53 这样的格式
        protocol_port = str(x[1]) + '/' + str(x[0])
        # 把应用清单写入protocol_list
        # 在写入前, 找到 '协议/端口' 所对应的应用名称, 如果没有找到保持原样
        protocol_list.append(protocol_map.get(protocol_port, protocol_port))
        # 把应用对应的字节数,写入protocol_bytes
        protocol_bytes.append(bytes_sum)

        # 把应用和相应的字节数 通过 zip压缩到一起
        # [('HTTP', 1234), ('FTP', 3444), ...]
        zip_list = [x for x in zip(protocol_list, protocol_bytes)]

        # 通过sorted + lambda 排序, 排序键值为字节数
        sorted_pro_data_list = sorted(zip_list, key=lambda x: x[1], reverse=True)
        # 把排序后的列表,继续分开到应用清单protocol_list和字节数清单protocol_bytes
        protocol_list = [x[0] for x in sorted_pro_data_list]
        protocol_bytes = [x[1] for x in sorted_pro_data_list]
    # 如果应用数超过5, 只截取前五
    if len(protocol_list) > 5:
        labels = protocol_list[:5]
        datas = protocol_bytes[:5]
    else:  # 如果应用数量不够5个,保留现有列表
        labels = protocol_list
        datas = protocol_bytes

    colors = ['#ff0000', '#ffff00', '#228b22', '#3342FF', '#524b22']  # 图表颜色码列表
    # 返回JSON数据,颜色,应用名列表, 应用字节数
    return JsonResponse({'colors': colors, 'labels': labels, 'datas': datas})


@login_required()
def netflow_top_ip(request):  # 为Netflow协议分析的"最大流量IP Top 5"返回JSON数据
    # 连接数据库
    # 后期推荐修改为Django的数据库查询方案
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    # 查询Netflow数据库, 在Netflow监控周期内的源IP地址信息, 找到出现的源IP地址
    cursor.execute("select src_ip from qytdb_netflow where date > CURRENT_TIMESTAMP - INTERVAL '" + str(getinterval_netflow()) + " hours' group by src_ip")
    yourresults = cursor.fetchall()

    ip_list = []

    # 找到出现的源IP地址
    for dbinfo in yourresults:
        ip_list.append(dbinfo)

    bytes_list = []
    for x in ip_list:
        # 提取特定源IP地址的入向字节数
        sqlcmd = "select in_bytes from qytdb_netflow where src_ip='" + x[0] + "' and date > CURRENT_TIMESTAMP - INTERVAL '" + str(getinterval_netflow()) + " hours'"
        cursor.execute(sqlcmd)
        yourresults = cursor.fetchall()
        bytes_sum = 0
        # 把每一个源IP的字节数加起来
        for dbinfo in yourresults:
            bytes_sum += dbinfo[0]

        # 把每一个源IP地址的字节总数添加到bytes_list中
        bytes_list.append(bytes_sum)

    # 把源IP地址和相应的字节数 通过 zip压缩到一起
    # [('10.1.1.1', 1234), ('10.1.1.2', 3444), ...]
    zip_list = [x for x in zip(ip_list, bytes_list)]

    # 通过sorted + lambda 排序, 排序键值为字节数
    sorted_ip_bytes_list = sorted(zip_list, key=lambda x: x[1], reverse=True)

    # 把排序后的列表,继续分开到源IP清单ip_list和字节数清单bytes_bytes
    ip_list = [x[0] for x in sorted_ip_bytes_list]
    bytes_list = [x[1] for x in sorted_ip_bytes_list]

    # 如果源IP数超过5, 只截取前五
    if len(ip_list) > 5:
        labels = ip_list[:5]
        datas = bytes_list[:5]
    else:  # 如果源IP数量不够5个,保留现有列表
        labels = ip_list
        datas = bytes_list

    colors = ['#ff0000', '#ffff00', '#228b22', '#3342FF', '#524b22']  # 图表颜色码列表
    # 返回JSON数据,颜色,源IP列表, 源IP累计字节数
    return JsonResponse({'colors': colors, 'labels': labels, 'datas': datas})


