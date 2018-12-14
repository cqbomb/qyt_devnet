#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
import pg8000
from qyt_devnet_0_snmp_get import snmpv2_get
from qyt_devnet_0_ssh import ssh_sure_shell_login

psql_ip = "192.168.1.11"
psql_username = "qytangdbuser"
psql_password = "Cisc0123"
psql_db_name = "qytangdb"
ssh_username = "admin"
ssh_password = "Cisc0123"


def reachable_test():
    conn = pg8000.connect(host=psql_ip, user=psql_username, password=psql_password, database=psql_db_name)
    cursor = conn.cursor()
    cursor.execute("select ip, type, name, snmp_ro_community, ssh_username, ssh_password, enable_password from qytdb_devicedb")
    result = cursor.fetchall()
    for device in result:
        snmp_reachable = "False"
        ssh_reachable = "False"
        try:
            if "SNMPv2-MIB::sysDescr.0" == snmpv2_get(str(device[0]), str(device[3]), "1.3.6.1.2.1.1.1.0", port=161)[0]:
                snmp_reachable = "True"
        except Exception:
            snmp_reachable = "False"
        if str(device[1]) == "switch" or str(device[1]) == "Router":
            if ssh_sure_shell_login(str(device[0]), str(device[1]), str(device[4]), str(device[5])):
                ssh_reachable = "True"
        elif str(device[1]) == "ASA":
            if ssh_sure_shell_login(str(device[0]), str(device[1]), str(device[4]), str(device[5]), str(device[6])):
                ssh_reachable = "True"
        cursor.execute("UPDATE qytdb_device_reachable SET snmp_reachable = '" + snmp_reachable + "', ssh_reachable = '" + ssh_reachable + "' WHERE name = '" + str(device[2]) + "'")
        conn.commit()


if __name__ == '__main__':
    reachable_test()
