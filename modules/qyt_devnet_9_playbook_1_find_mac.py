#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from qyt_devnet_0_DB_login import psql_ip, psql_username, psql_password, psql_db_name
from qyt_devnet_0_ssh import ssh_singlecmd
import pg8000
import re


# 这只是测试代码! 并未被使用!真正使用的代码位于qyt_playbook.py
def get_device_login_info(ip):
    # 连接数据库
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    # 查询数据库qytdb_devicedb,获取ip, type, name, snmp_ro_community, ssh_username, ssh_password, enable_password等信息
    cursor.execute("SELECT * FROM qytdb_devicedb where ip='" + ip + "'")
    result = cursor.fetchall()[0]
    return result[8], result[9]


def get_all_sw_login_info():
    # 连接数据库
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    # 查询数据库qytdb_devicedb,获取ip, type, name, snmp_ro_community, ssh_username, ssh_password, enable_password等信息
    cursor.execute("SELECT * FROM qytdb_devicedb where type='switch'")
    result = cursor.fetchall()
    switch_list = []
    for x in result:
        switch_list.append((str(x[2]), x[8], x[9], x[1]))

    return switch_list


def if_ip_reachable(seed_ip, ip):
    ip_reachable = False
    arp_reachable = False
    cmd_ping = 'ping ' + ip
    seed_device_login_info = get_device_login_info(seed_ip)
    seed_username = seed_device_login_info[0]
    seed_password = seed_device_login_info[1]
    ping_result = ssh_singlecmd(seed_ip, seed_username, seed_password, cmd_ping)
    for x in ping_result.split('\n')[-3:]:
        try:
            result = re.match('.*, (\d+) packets received,.*', x.strip()).groups()
            if int(result[0]) >= 1:
                ip_reachable = True

        except Exception:
            continue
    cmd_arp = 'show ip arp ' + ip
    arp_result = ssh_singlecmd(seed_ip, seed_username, seed_password, cmd_arp).split('\n')[-2].strip()
    try:
        arp = re.match(ip + '\s+\d\d:\d\d:\d\d\s+([0-9a-f]{4}.[0-9a-f]{4}\.[0-9a-f]{4})\s+.*', arp_result).groups()[0]
        arp_reachable = arp
        return ip_reachable, arp_reachable
    except AttributeError:
        return ip_reachable, arp_reachable


def mac_if(ip, mac):
    cmd_mac_if = 'show system internal l2fwder mac | in ' + mac
    device_login_info = get_device_login_info(ip)
    username = device_login_info[0]
    password = device_login_info[1]
    mac_if_result = ssh_singlecmd(ip, username, password, cmd_mac_if).strip()
    try:
        if_result = re.match('.*\s+(\w+.*\d)$', mac_if_result).groups()[0]
        return if_result
    except AttributeError:
        return False


def cdp_info(ip, ifname):
    cmd_cdp = 'show cdp neighbors interface ' + ifname +' detail'
    device_login_info = get_device_login_info(ip)
    username = device_login_info[0]
    password = device_login_info[1]
    cdp_if_result = ssh_singlecmd(ip, username, password, cmd_cdp).strip()
    re_cdp_result = re.match('Note: CDP Neighbor entry not found', cdp_if_result.strip())
    if re_cdp_result:
        return False
    else:
        for x in cdp_if_result.split('\n'):
            ip_address = re.match('IPv4 Address: (.*)', x.strip())
            if ip_address:
                return ip_address.groups()[0]


def cdp_all_if(ip):
    cmd_cdp = 'show cdp neighbors'
    device_login_info = get_device_login_info(ip)
    username = device_login_info[0]
    password = device_login_info[1]
    cdp_if_result = ssh_singlecmd(ip, username, password, cmd_cdp).strip()
    if_list = []
    for x in cdp_if_result.split('\n'):

        re_result = re.match('^(\w+.*\d+)\s+\d+.*', x.strip())
        if re_result:
            if re.match('.+\s+\w+\d', re_result.groups()[0]):
                # print(re_result.groups()[0].split())
                if_list.append(re_result.groups()[0].split()[1].strip())
            else:
                if_list.append(re_result.groups()[0])

    return list(set(if_list))


def find_ip_device_if(seed_ip, ip):
    mac_address = if_ip_reachable(seed_ip, ip)[1]
    # print(mac_address)
    if mac_address:
        pass
    else:
        return False
    switch_list = get_all_sw_login_info()
    for switch in switch_list:
        ifname = mac_if(switch[0], mac_address)
        # print(ifname)
        if ifname:
            if ifname in cdp_all_if(switch[0]):
                continue
            else:
                return switch[3], ifname


if __name__ == '__main__':
    # print(if_ip_reachable("192.168.1.103", "10.1.1.1"))
    # print(mac_if('192.168.1.103', '0050.56ab.fa2c'))
    # print(cdp_info('192.168.1.103', 'Eth1/1'))
    # print(cdp_all_if('192.168.1.103'))
    print(find_ip_device_if("192.168.1.103", "10.1.1.2"))
    # get_all_sw_login_info()
