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


# 执行单个SSH命令的函数
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


# 查询数据库, 返回特定IP地址的SSH登录用户名和密码
def get_device_login_info(ip):
    device_login_info = Devicedb.objects.get(ip=ip)
    return device_login_info.ssh_username, device_login_info.ssh_password


# 查询数据库, 返回所有交换机的IP地址,SSH登录用户名和SSH密码
def get_all_sw_login_info():
    switch_login_info = Devicedb.objects.filter(type='Nexus Switch')
    switch_list = []
    for x in switch_login_info:
        switch_list.append((str(x.ip), x.ssh_username, x.ssh_password, x.name))
    return switch_list


# 判断IP地址是否可达, 如果可达获取IP对应的MAC地址信息, 便于后续查询
def if_ip_reachable(seed_ip, ip):
    # 默认IP不可达为 False(其实是Ping的可达性)
    ip_reachable = False
    # 默认ARP不可达为 False
    arp_reachable = False
    # 准备执行的ping命令, ping <ip>
    cmd_ping = 'ping ' + ip
    # 获取seed设备,核心三层交换机(Core_SW)的SSH登录用户名和密码
    seed_device_login_info = get_device_login_info(seed_ip)
    seed_username = seed_device_login_info[0]
    seed_password = seed_device_login_info[1]
    # 执行ping,并且获取ping的结果
    ping_result = ssh_singlecmd(seed_ip, seed_username, seed_password, cmd_ping)
    # 我们只对ping结果的最后三行进行正则表达式的匹配
    # ping通的最后三行
    # 5 packets transmitted, 5 packets received, 0.00% packet loss
    # round-trip min/avg/max = 14.839/20.634/37.094 ms
    # 空行

    # ping不通的最后三行
    # --- 10.1.1.1 ping statistics ---
    # 5 packets transmitted, 0 packets received, 100.00% packet loss
    # 空行

    # 我关注的是"packets received"的数量
    for x in ping_result.split('\n')[-3:]:
        try:
            # 5 packets transmitted, 5 packets received, 0.00% packet loss
            result = re.match('.*, (\d+) packets received,.*', x.strip()).groups()
            if int(result[0]) >= 1:  # 如果收到的包大于等于1, 表示IP可达(ping可达)
                ip_reachable = True

        except Exception:
            continue
    # 当然现在很多设备都不让ping, 所以需要再进行ARP的确认
    # 下面是查询ARP的命令, Nexus交换机需要使用show ip arp这个命令,与IOS略有不同
    cmd_arp = 'show ip arp ' + ip
    # 执行查询ARP的操作, 并且获取返回结果
    # Address         Age       MAC Address     Interface
    # 10.1.1.12       00:00:16  0050.56ab.fa2c
    arp_result = ssh_singlecmd(seed_ip, seed_username, seed_password, cmd_arp).split('\n')[-2].strip()
    try:
        # 正则表达式匹配"10.1.1.12       00:00:16  0050.56ab.fa2c "中的MAC地址
        arp = re.match(ip + '\s+\d\d:\d\d:\d\d\s+([0-9a-f]{4}.[0-9a-f]{4}\.[0-9a-f]{4})\s+.*', arp_result).groups()[0]
        arp_reachable = arp  # 如果能够获取MAC地址, 表示ARP可达
        # 返回IP可达性(这个其实并不重要), 与ARP解析的MAC地址
        return ip_reachable, arp_reachable
    except AttributeError:
        return ip_reachable, arp_reachable


def mac_if(ip, mac):  # 查看特定MAC所在交换机接口
    # Nexus9000的模拟器需要使用'show system internal l2fwder mac'来查询交换机的CAM表
    cmd_mac_if = 'show system internal l2fwder mac | in ' + mac
    # 获取特定交换机的SSH登录用户名和密码
    device_login_info = get_device_login_info(ip)
    username = device_login_info[0]
    password = device_login_info[1]
    # SSH登录到交换机,并且执行查询特定MAC地址所在接口的操作
    # Core_SW# show system internal l2fwder mac | in 0050.56ab.fa2c
    # *    10    0050.56ab.fa2c   dynamic   1d12h   F     F     Eth1/1
    mac_if_result = ssh_singlecmd(ip, username, password, cmd_mac_if).strip()
    try:
        # 找到'*    10    0050.56ab.fa2c   dynamic   1d12h   F     F     Eth1/1 '中的接口名称
        if_result = re.match('.*\s+(\w+.*\d)$', mac_if_result).groups()[0]
        # 如果找到, 返回接口名称
        return if_result
    except AttributeError:
        return False  # 如果找不到, 返回False


def cdp_info(ip, ifname):  # 查看特定接口CDP邻居的IP地址
    # 查看特定接口CDP邻居详细信息
    cmd_cdp = 'show cdp neighbors interface ' + ifname +' detail'
    # 获取特定设备的SSH登录用户名和密码
    device_login_info = get_device_login_info(ip)
    username = device_login_info[0]
    password = device_login_info[1]
    # 登录到设备执行 查看特定接口CDP邻居详细信息 的操作
    cdp_if_result = ssh_singlecmd(ip, username, password, cmd_cdp).strip()
    # Core_SW# sh cdp neighbors interface e1/1 detail
    # ----------------------------------------
    # Device ID:SW1(93SZHUQBJ9C)
    # System Name: SW1
    #
    # Interface address(es):
    #     IPv4 Address: 10.1.1.101
    # Platform: N9K-NXOSV, Capabilities: Router Switch IGMP Filtering Supports-STP-Dispute
    # Interface: Ethernet1/1, Port ID (outgoing port): Ethernet1/1
    # Holdtime: 139 sec
    #
    # Version:
    # Cisco Nexus Operating System (NX-OS) Software, Version 7.0(3)I5(1)
    #
    # Advertisement Version: 2
    #
    # Native VLAN: 1
    # Duplex: full
    #
    # MTU: 1500
    # Mgmt address(es):
    #     IPv4 Address: 192.168.1.101

    # 如果匹配上'Note: CDP Neighbor entry not found'表示没有CDP邻居
    re_cdp_result = re.match('Note: CDP Neighbor entry not found', cdp_if_result.strip())
    if re_cdp_result:
        return False
    else:  # 如果有CDP邻居, 通过正则表达式匹配找到邻居的IP地址
        for x in cdp_if_result.split('\n'):
            ip_address = re.match('IPv4 Address: (.*)', x.strip())
            if ip_address:
                return ip_address.groups()[0]


def cdp_all_if(ip):  # 找到所有的拥有CDP邻居的接口清单
    # 执行的命令'show cdp neighbors'
    cmd_cdp = 'show cdp neighbors'
    # 获取登录特定设备的SSH用户名和密码
    device_login_info = get_device_login_info(ip)
    username = device_login_info[0]
    password = device_login_info[1]
    # SSH登录到设备执行 'show cdp neighbors' 的命令
    cdp_if_result = ssh_singlecmd(ip, username, password, cmd_cdp).strip()
    # Core_SW# show cdp nei
    # Capability Codes: R - Router, T - Trans-Bridge, B - Source-Route-Bridge
    #                   S - Switch, H - Host, I - IGMP, r - Repeater,
    #                   V - VoIP-Phone, D - Remotely-Managed-Device,
    #                   s - Supports-STP-Dispute
    #
    # Device-ID          Local Intrfce  Hldtme Capability  Platform      Port ID
    # SW1(93SZHUQBJ9C)    mgmt0          159    R S s     N9K-NXOSV     mgmt0
    # Core_GW.qytang.com(神奇的地方, 这个地方真的有换行)
    #                     mgmt0          155    R B       Linux Unix    Eth0/0
    # Access_SW2(9P3GZ7F6PEF)
    #                     mgmt0          160    R S s     N9K-NXOSV     mgmt0
    # SW1(93SZHUQBJ9C)    Eth1/1         137    R S I s   N9K-NXOSV     Eth1/1
    # Access_SW2(9P3GZ7F6PEF)
    #                     Eth1/2         142    R S I s   N9K-NXOSV     Eth1/1

    if_list = []
    for x in cdp_if_result.split('\n'):
        re_result = re.match('^(\w+.*\d+)\s+\d+.*', x.strip())
        if re_result:
            if re.match('.+\s+\w+\d', re_result.groups()[0]):
                # 如果是这样'SW1(93SZHUQBJ9C)    Eth1/1' 要后面[1]号部分
                if_list.append(re_result.groups()[0].split()[1].strip())
            else:  # 如果是这样'Eth1/2'就直接返回
                if_list.append(re_result.groups()[0])

    return list(set(if_list))  # 使用set消除重复项目


def find_ip_device_if(seed_ip, ip):  # 找到IP所在接口, 最终程序!!!
    # 获取IP对应的MAC地址
    mac_address = if_ip_reachable(seed_ip, ip)[1]

    if mac_address:
        pass  # 如果MAC地址存在就继续执行
    else:  # 如果MAC地址不存在就直接返回False
        return False
    switch_list = get_all_sw_login_info()  # 获取所有交换机的登录信息
    for switch in switch_list:
        # 在每一个交换机查询特定MAC在CAM表中对应的接口
        ifname = mac_if(switch[0], mac_address)
        # 如果找到接口
        if ifname:
            if ifname in cdp_all_if(switch[0]):  # 如果接口出现在CDP邻居接口清单(级联口)就忽略此接口
                continue
            else:  # 否则就返回设备名称与接口名称
                return switch[3], ifname


@login_required()
def find_if(request):
    if request.method == 'POST':
        form = FindifForm(request.POST)
        # 如果请求为POST,并且Form校验通过
        if form.is_valid():
            ip = request.POST.get('ip'),  # 获取客户输入需要查找的IP地址
            find_result = find_ip_device_if("192.168.1.103", ip[0])  # 查找IP地址所在接口
            if find_result:  # 如果找到返回'find_if_result_good.html'页面,并给客户展示结果
                return render(request, 'find_if_result_good.html', {'devicename': find_result[0], 'ifname': find_result[1]})
            else:  # 如果没有找到,返回'find_if_result_bad.html'页面,并告诉客户特定IP地址未找到
                return render(request, 'find_if_result_bad.html', {'ip': ip[0]})
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            return render(request, 'find_if.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 显示表单内容给客户
        form = FindifForm()
        return render(request, 'find_if.html', {'form': form})
