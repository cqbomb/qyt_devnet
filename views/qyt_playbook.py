#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from qytdb.forms import FindifForm
from qytdb.models import Devicedb
import re
import paramiko
import pg8000
psql_ip = "192.168.1.11"
psql_username = "qytangdbuser"
psql_password = "Cisc0123"
psql_db_name = "qytangdb"


def ssh_singlecmd(ip, username, password, cmd):
    try:
        ssh = paramiko.SSHClient()  # 创建SSH Client
        ssh.load_system_host_keys()  # 加载系统SSH密钥
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 添加新的SSH密钥
        ssh.connect(ip, port=22, username=username, password=password, timeout=5, compress=True)  # SSH连接
        stdin, stdout, stderr = ssh.exec_command(cmd)  # 执行命令
        x = stdout.read().decode()  # 读取回显
        ssh.close()
        return x

    except Exception as e:
        print('%stErrorn %s' % (ip, e))


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


def find_if(request):
    if request.method == 'POST':
        form = FindifForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把新添加的虚拟机信息写入数据库
        if form.is_valid():
            ip = request.POST.get('ip'),
            find_result = find_ip_device_if("192.168.1.103", ip[0])
            if find_result:
                return render(request, 'find_if_result_good.html', {'devicename': find_result[0], 'ifname': find_result[1]})
            else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
                return render(request, 'find_if_result_bad.html', {'ip': ip[0]})
    else:  # 如果不是POST,就是GET,表示为初始访问, 显示表单内容给客户
        form = FindifForm()
        return render(request, 'find_if.html', {'form': form})


if __name__ == "__main__":
    print(find_ip_device_if("192.168.1.103", "10.1.1.2"))