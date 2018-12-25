#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from modules.qyt_devnet_0_ssh import ssh_singlecmd, ssh_multicmd, ssh_multicmd_asa
import re
import pg8000
import hashlib
from datetime import datetime
from qyt_devnet_0_DB_login import psql_ip, psql_username, psql_password, psql_db_name


# 获取特定设备的配置与MD5值, 这个函数会在添加设备的时候使用, 用于做初始化备份
def get_config_md5_from_device(ip, ssh_username, ssh_password, type, enable_password='Cisc0123'):
    if type == 'Router':  # 如果设备为路由器
        # 获取设备show run
        run_config_raw = ssh_singlecmd(ip, ssh_username, ssh_password, 'show run')
        list_run_config = run_config_raw.split('\n')
        location = 0
        host_location = 0  # 用来找到hostname出现的位
        for i in list_run_config:
            if re.match('.*hostname .*', i):
                host_location = location  # 定位hostname所在位置
            else:
                location += 1
        list_run_config = list_run_config[host_location:]  # 截取hostname开始往后的部分
        run_config = '\n'.join(list_run_config)  # 再次还原为字串形式的配置

        # 计算获取配置的MD5值
        m = hashlib.md5()
        m.update(run_config.encode())
        md5_value = m.hexdigest()

        # 返回配置与MD5值
        return run_config, md5_value

    elif type == 'switch':  # 如果设备为交换机
        # 获取设备show run
        run_config_raw = ssh_singlecmd(ip, ssh_username, ssh_password, 'show run')
        list_run_config = run_config_raw.split('\n')
        location = 0
        host_location = 0  # 用来找到hostname出现的位
        for i in list_run_config:
            if re.match('.*hostname .*', i):
                host_location = location  # 定位hostname所在位置
            else:
                location += 1
        list_run_config = list_run_config[host_location:]  # 截取hostname开始往后的部分
        run_config = '\n'.join(list_run_config)  # 再次还原为字串形式的配置

        # 计算获取配置的MD5值
        m = hashlib.md5()
        m.update(run_config.encode())
        md5_value = m.hexdigest()

        # 返回配置与MD5值
        return run_config, md5_value

    elif type == 'ASA':  # 如果设备为ASA
        # 获取设备show run, 注意获取ASA配置的方法不一样
        run_config_raw = ssh_multicmd_asa(ip, ssh_username, ssh_password,
                                          ['enable', enable_password, 'terminal pager 0', 'more system:running-config'])
        list_run_config = run_config_raw.split('\n')
        location = 0
        host_location = 0  # 用来找到hostname出现的位置
        for i in list_run_config:
            if re.match('^hostname .*', i):  # 注意匹配hostname的方法不一样,因为配置中会多次出现hostname
                host_location = location  # 定位hostname所在位置
            else:
                location += 1
        list_run_config = list_run_config[host_location:-4]  # 截取hostname开始往后的部分
        run_config = '\n'.join(list_run_config)  # 再次还原为字串形式的配置

        # 计算获取配置的MD5值
        m = hashlib.md5()
        m.update(run_config.encode())
        md5_value = m.hexdigest()

        # 返回配置与MD5值
        return run_config, md5_value


if __name__ == '__main__':
    # print(get_config_md5_from_device('192.168.1.101', 'admin', 'Cisc0123', 'switch'))
    # print(get_config_md5_from_device('192.168.1.105', 'admin', 'Cisc0123', 'Router'))
    print(get_config_md5_from_device('192.168.1.104', 'admin', 'Cisc0123', 'ASA', 'Cisc0123'))