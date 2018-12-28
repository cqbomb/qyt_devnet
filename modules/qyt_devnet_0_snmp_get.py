#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


from pysnmp.hlapi import *
import pg8000
from qyt_devnet_0_DB_login import psql_ip, psql_username, psql_password, psql_db_name

def snmpv2_get(ip, community, oid, port=161):
    # varBinds是列表，列表中的每个元素的类型是ObjectType（该类型的对象表示MIB variable）
    errorIndication, errorStatus, errorindex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),  # 配置community
               UdpTransportTarget((ip, port)),  # 配置目的地址和端口号
               ContextData(),
               ObjectType(ObjectIdentity(oid))  # 读取的OID
               )
    )
    # 错误处理
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (
            errorStatus,
            errorindex and varBinds[int(errorindex) - 1][0] or '?'
        )
              )
    # 如果返回结果有多行,需要拼接后返回
    result = ""
    for varBind in varBinds:
        result = result + varBind.prettyPrint() # 返回结果！
    # 返回的为一个元组,OID与字符串结果
    return result.split("=")[0].strip(), result.split("=")[1].strip()


def get_mem_cpu(ip, type, community):
    # 连接PSQL数据库
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    cursor.execute("select mem_used_oid, mem_free_oid, cpu_oid from qytdb_devicetypesnmp where type='" + type + "'")
    result = cursor.fetchall()
    used = int(snmpv2_get(ip, community, result[0][0], port=161)[1])
    # Nexus MEM 闲置
    free = int(snmpv2_get(ip, community, result[0][1], port=161)[1])
    # Nexus CPU 1 min
    cpu = int(snmpv2_get(ip, community, result[0][2], port=161)[1])
    # 返回内存利用率与CPU利用率
    return int(float(used/(free + used)) * 100), cpu


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    device_ip = "192.168.1.105"
    asa_ip = "192.168.1.104"
    nexus_ip = "192.168.1.101"
    community = "qytangro"
    # 系统描述
    # print(snmpv2_get(device_ip, community, "1.3.6.1.2.1.1.1.0", port=161))
    # # 联系人
    # print(snmpv2_get(device_ip, community, "1.3.6.1.2.1.1.4.0", port=161))
    # # 主机名
    # print(snmpv2_get(device_ip, community, "1.3.6.1.2.1.1.5.0", port=161))
    # # 地点
    # print(snmpv2_get(device_ip, community, "1.3.6.1.2.1.1.6.0", port=161))
    print(get_mem_cpu(device_ip, "IOS Router", community))
    print(get_mem_cpu(nexus_ip, "Nexus Switch", community))
    print(get_mem_cpu(asa_ip, "ASA Firewall", community))



