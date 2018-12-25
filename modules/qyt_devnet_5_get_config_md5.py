#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from qyt_devnet_0_ssh import ssh_singlecmd, ssh_multicmd, ssh_multicmd_asa
import re
import pg8000
import hashlib
from datetime import datetime
from qyt_devnet_0_DB_login import psql_ip, psql_username, psql_password, psql_db_name


def get_md5_config():
    # 连接数据库
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    # 查询数据库qytdb_devicedb,获取ip, type, name, snmp_ro_community, ssh_username, ssh_password, enable_password等信息
    cursor.execute("select ip, type, name, snmp_ro_community, ssh_username, ssh_password, enable_password from qytdb_devicedb")
    result = cursor.fetchall()
    for device in result:
        if device[1] == 'Router':  # 如果设备是路由器
            # 获取设备show run
            run_config_raw = ssh_singlecmd(str(device[0]), device[4], device[5], 'show run')
            list_run_config = run_config_raw.split('\n')
            location = 0
            host_location = 0  # 用来找到hostname出现的位置
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
            # 获取最近一次保存配置的MD5值,注意添加设备的时候就会做一次备份!
            # order by date desc limit 1 查询最近一次记录
            cursor.execute("select hash from qytdb_deviceconfig where name = '" + device[2] + "' order by date desc limit 1")
            result = cursor.fetchall()
            if result[0][0] == md5_value:  # 如果本次配置的MD5值,与上一次备份配置的MD5值相同!略过此次操作
                continue
            else:
                # 如果本次配置的MD5值,与上一次备份配置的MD5值不相同,备份配置与MD5值到数据库
                sqlcmd = "INSERT INTO qytdb_deviceconfig (name, hash, config, date) VALUES ('" + device[2] + "', '" + md5_value + "', '" + run_config + "', '" + str(datetime.now()) + "')"
                cursor.execute(sqlcmd)
                conn.commit()

        elif device[1] == 'switch':  # 如果设备是交换机
            # 获取设备show run
            run_config_raw = ssh_singlecmd(str(device[0]), device[4], device[5], 'show run')
            list_run_config = run_config_raw.split('\n')
            location = 0
            host_location = 0  # 用来找到hostname出现的位置
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

            # 获取最近一次保存配置的MD5值,注意添加设备的时候就会做一次备份!
            # order by date desc limit 1 查询最近一次记录
            cursor.execute("select hash from qytdb_deviceconfig where name = '" + device[2] + "' order by date desc limit 1")
            result = cursor.fetchall()
            if result[0][0] == md5_value:  # 如果本次配置的MD5值,与上一次备份配置的MD5值相同!略过此次操作
                continue
            else:
                # 如果本次配置的MD5值,与上一次备份配置的MD5值不相同,备份配置与MD5值到数据库
                sqlcmd = "INSERT INTO qytdb_deviceconfig (name, hash, config, date) VALUES ('" + device[2] + "', '" + md5_value + "', '" + run_config + "', '" + str(datetime.now()) + "')"
                cursor.execute(sqlcmd)
                conn.commit()

        elif device[1] == 'ASA':  # 如果设备是ASA
            # 获取设备show run, 注意获取ASA配置的方法不一样
            run_config_raw = ssh_multicmd_asa(str(device[0]), device[4], device[5], ['enable', device[6], 'terminal pager 0', 'more system:running-config'])
            list_run_config = run_config_raw.split('\n')
            location = 0
            host_location = 0  # 用来找到hostname出现的位置
            for i in list_run_config:
                if re.match('^hostname .*', i):  # 注意匹配hostname的方法不一样,因为配置中会多次出现hostname
                    host_location = location  # 定位hostname所在位置
                else:
                    location += 1
            list_run_config = list_run_config[host_location:-4]  # 截取hostname开始往后的部分, 去除最后一些无用部分
            run_config = '\n'.join(list_run_config)  # 再次还原为字串形式的配置

            # 计算获取配置的MD5值
            m = hashlib.md5()
            m.update(run_config.encode())
            md5_value = m.hexdigest()

            # 获取最近一次保存配置的MD5值,注意添加设备的时候就会做一次备份!
            # order by date desc limit 1 查询最近一次记录
            cursor.execute("select hash from qytdb_deviceconfig where name = '" + device[2] + "' order by date desc limit 1")
            result = cursor.fetchall()
            if result[0][0] == md5_value:  # 如果本次配置的MD5值,与上一次备份配置的MD5值相同!略过此次操作
                continue
            else:
                # 如果本次配置的MD5值,与上一次备份配置的MD5值不相同,备份配置与MD5值到数据库
                sqlcmd = "INSERT INTO qytdb_deviceconfig (name, hash, config, date) VALUES ('" + device[2] + "', '" + md5_value + "', '" + run_config + "', '" + str(datetime.now()) + "')"
                cursor.execute(sqlcmd)
                conn.commit()


if __name__ == '__main__':
    get_md5_config()
