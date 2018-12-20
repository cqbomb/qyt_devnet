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

psql_ip = "192.168.1.11"
psql_username = "qytangdbuser"
psql_password = "Cisc0123"
psql_db_name = "qytangdb"


def get_config_md5_from_device(ip, ssh_username, ssh_password, type, enable_password='Cisc0123'):
    if type == 'Router':
        run_config_raw = ssh_singlecmd(ip, ssh_username, ssh_password, 'show run')
        list_run_config = run_config_raw.split('\n')
        location = 0
        host_location = 0
        for i in list_run_config:
            if re.match('.*hostname .*', i):
                host_location = location  # 定位hostname所在位置
            else:
                location += 1
        list_run_config = list_run_config[host_location:]  # 截取hostname开始往后的部分
        run_config = '\n'.join(list_run_config)  # 再次还原为字串形式的配置

        m = hashlib.md5()
        m.update(run_config.encode())
        md5_value = m.hexdigest()

        return run_config, md5_value

    elif type == 'switch':
        run_config_raw = ssh_singlecmd(ip, ssh_username, ssh_password, 'show run')
        list_run_config = run_config_raw.split('\n')
        location = 0
        host_location = 0
        for i in list_run_config:
            if re.match('.*hostname .*', i):
                host_location = location  # 定位hostname所在位置
            else:
                location += 1
        list_run_config = list_run_config[host_location:]  # 截取hostname开始往后的部分
        run_config = '\n'.join(list_run_config)  # 再次还原为字串形式的配置

        m = hashlib.md5()
        m.update(run_config.encode())
        md5_value = m.hexdigest()

        return run_config, md5_value

    elif type == 'ASA':
        run_config_raw = ssh_multicmd_asa(ip, ssh_username, ssh_password,
                                          ['enable', enable_password, 'terminal pager 0', 'more system:running-config'])
        list_run_config = run_config_raw.split('\n')
        location = 0
        host_location = 0
        for i in list_run_config:
            if re.match('^hostname .*', i):
                host_location = location  # 定位hostname所在位置
            else:
                location += 1
        list_run_config = list_run_config[host_location:-4]  # 截取hostname开始往后的部分
        run_config = '\n'.join(list_run_config)  # 再次还原为字串形式的配置

        m = hashlib.md5()
        m.update(run_config.encode())
        md5_value = m.hexdigest()

        return run_config, md5_value


if __name__ == '__main__':
    # print(get_config_md5_from_device('192.168.1.101', 'admin', 'Cisc0123', 'switch'))
    # print(get_config_md5_from_device('192.168.1.105', 'admin', 'Cisc0123', 'Router'))
    print(get_config_md5_from_device('192.168.1.104', 'admin', 'Cisc0123', 'ASA', 'Cisc0123'))