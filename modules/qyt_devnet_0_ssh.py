#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


import paramiko
import time
import re


def ssh_multicmd(ip, username, password, cmd_list, verbose=True):
    ssh = paramiko.SSHClient()  # 创建SSH Client
    ssh.load_system_host_keys()  # 加载系统SSH密钥
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 添加新的SSH密钥
    ssh.connect(ip, port=22, username=username, password=password, timeout=5, compress=True)  # SSH连接

    chan = ssh.invoke_shell()  # 激活交互式shell
    time.sleep(1)
    x = chan.recv(2048).decode()  # 接收回显信息
    cmd_list_len = len(cmd_list)
    i = 1
    for cmd in cmd_list:  # 读取命令
        chan.send(cmd.encode())  # 执行命令，注意字串都需要编码为二进制字串
        chan.send(b'\n')  # 一定要注意输入回车
        time.sleep(2)  # 由于有些回显可能过长，所以可以考虑等待更长一些时间
        x = chan.recv(40960).decode()  # 读取回显，有些回想可能过长，请把接收缓存调大
        # 此处对源码进行了调整,只是显示最后一个命令的回显
        if verbose and i == cmd_list_len:
            return x.split('\r\n')[1]  # 打印回显
        i += 1

    chan.close()  # 退出交互式shell
    ssh.close()  # 退出ssh会话


def ssh_multicmd_asa(ip, username, password, cmd_list, verbose=True):
    ssh = paramiko.SSHClient()  # 创建SSH Client
    ssh.load_system_host_keys()  # 加载系统SSH密钥
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 添加新的SSH密钥
    ssh.connect(ip, port=22, username=username, password=password, timeout=5, compress=True)  # SSH连接

    chan = ssh.invoke_shell()  # 激活交互式shell
    time.sleep(2)
    x = chan.recv(2048).decode()  # 接收回显信息
    cmd_list_len = len(cmd_list)
    i = 1
    for cmd in cmd_list:  # 读取命令
        chan.send(cmd.encode())  # 执行命令，注意字串都需要编码为二进制字串
        chan.send(b'\n')  # 一定要注意输入回车
        time.sleep(3)  # 由于有些回显可能过长，所以可以考虑等待更长一些时间
        x = chan.recv(40960).decode()  # 读取回显，有些回想可能过长，请把接收缓存调大
        # 此处对源码进行了调整,只是显示最后一个命令的回显
        if verbose and i == cmd_list_len:
            return x  # 打印回显
        i += 1

    chan.close()  # 退出交互式shell
    ssh.close()  # 退出ssh会话


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


def ssh_sure_shell_login(ip, type, username, password, enable_password="Cisc0123"):
    # 判断设备类型为交换机或者路由器
    if type == "switch" or type == "Router":
        try:
            # 确认能够使用"show run | in hostname"命令
            # 并且回显有hostname信息
            result = ssh_singlecmd(ip, username, password, 'show run | in hostname')
            if re.match("^hostname \w+", result.strip()):
                return True
            else:
                return False
        except Exception:
            return False
    # 确认设备为ASA
    elif type == "ASA":
        try:
            # ASA由于默认并不能进入特权模式,所以需要敲enable,和enable密码
            result = ssh_multicmd(ip, username, password, ['enable', enable_password, 'show run | in hostname'])
            # 确认最后一个命令的输出中有hostname信息
            if re.match('^hostname \w+', result.strip()):
                return True
            else:
                return False
        except Exception:
            return False


if __name__ == '__main__':
    # 使用Linux解释器 & WIN解释器
    # print(ssh_sure_shell_login('192.168.1.101', 'switch', 'admin', 'Cisc0123'))
    # print(ssh_sure_shell_login('192.168.1.104', 'ASA', 'admin', 'Cisc0123', 'Cisc0123'))
    # print(ssh_sure_shell_login('192.168.1.105', 'Router', 'admin', 'Cisc0123'))
    print(ssh_multicmd_asa('192.168.1.104', 'admin', 'Cisc0123', ['enable', 'Cisc0123', 'terminal pager 0', 'show run']))

