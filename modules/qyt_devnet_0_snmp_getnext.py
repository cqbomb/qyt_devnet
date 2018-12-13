#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a


from pysnmp.entity.rfc3413.oneliner import cmdgen


def snmpv2_getnext(ip, community, oid, port=161):
    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorindex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData(community),  # 设置community
        cmdgen.UdpTransportTarget((ip, port)),  # 设置IP地址和端口号
        oid,  # 设置OID
    )
    # 错误处理
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorindex and varBinds[int(errorindex) - 1][0] or '?'
        )
              )

    result = []
    # varBindTable是个list，元素的个数可能有好多个。它的元素也是list，这个list里的元素是ObjectType，个数只有1个。
    for varBindTableRow in varBindTable:
        for item in varBindTableRow:
            result.append((item.prettyPrint().split("=")[0].strip(), item.prettyPrint().split("=")[1].strip()))
    return result


def get_ifs(ip, type, community):
    if type == "switch" or type == "Router":
        ifs_name_list_raw = snmpv2_getnext(ip, community, "1.3.6.1.2.1.2.2.1.2", port=161)
        ifs_bw_list_raw = snmpv2_getnext(ip, community, "1.3.6.1.2.1.2.2.1.5", port=161)
        ifs_in_list_raw = snmpv2_getnext(ip, community, "1.3.6.1.2.1.2.2.1.10", port=161)
        ifs_out_list_raw = snmpv2_getnext(ip, community, "1.3.6.1.2.1.2.2.1.16", port=161)
        ifs_name_list = [x[1] for x in ifs_name_list_raw]
        # print(ifs_name_list)
        ifs_bw_list = [x[1] for x in ifs_bw_list_raw]
        # print(ifs_bw_list)
        ifs_in_list = [x[1] for x in ifs_in_list_raw]
        # print(ifs_in_list)
        ifs_out_list = [x[1] for x in ifs_out_list_raw]
        # print(ifs_out_list)
        ifs_info_zip = zip(ifs_name_list, ifs_bw_list, ifs_in_list, ifs_out_list)
        ifs_info_list = []
        for if_info in ifs_info_zip:
            if if_info[2] == '0' and if_info[3] == '0':
                continue
            ifs_info_list.append(if_info)
        return ifs_info_list
    elif type == "ASA":
        ifs_name_list_raw = snmpv2_getnext(ip, community, "1.3.6.1.2.1.2.2.1.2", port=161)
        ifs_bw_list_raw = snmpv2_getnext(ip, community, "1.3.6.1.2.1.2.2.1.5", port=161)
        ifs_in_list_raw = snmpv2_getnext(ip, community, "1.3.6.1.2.1.2.2.1.10", port=161)
        ifs_out_list_raw = snmpv2_getnext(ip, community, "1.3.6.1.2.1.2.2.1.16", port=161)
        ifs_name_list = [x[1].replace("Adaptive Security Appliance '", "").replace("' interface", "") for x in ifs_name_list_raw]
        # print(ifs_name_list)
        ifs_bw_list = [x[1] for x in ifs_bw_list_raw]
        # print(ifs_bw_list)
        ifs_in_list = [x[1] for x in ifs_in_list_raw]
        # print(ifs_in_list)
        ifs_out_list = [x[1] for x in ifs_out_list_raw]
        # print(ifs_out_list)
        ifs_info_zip = zip(ifs_name_list, ifs_bw_list, ifs_in_list, ifs_out_list)
        ifs_info_list = []
        for if_info in ifs_info_zip:
            if if_info[2] == '0' and if_info[3] == '0':
                continue
            ifs_info_list.append(if_info)
        return ifs_info_list


if __name__ == "__main__":
    # 使用Linux解释器 & WIN解释器
    device_ip = "192.168.1.105"
    asa_ip = "192.168.1.104"
    nexus_ip = "192.168.1.103"
    community = "qytangro"
    # # 显示接口信息
    # print(snmpv2_getnext(device_ip, community, "1.3.6.1.2.1.2.2.1.2", port=161))
    # for x, y in snmpv2_getnext(device_ip, community, "1.3.6.1.2.1.2.2.1.2", port=161):
    #     print(x, y)
    # # 接口速率
    # print(snmpv2_getnext(device_ip, community, "1.3.6.1.2.1.2.2.1.5", port=161))
    #
    # # 进接口字节数
    # print(snmpv2_getnext(device_ip, community, "1.3.6.1.2.1.2.2.1.10", port=161))
    #
    # # 出接口字节数
    # print(snmpv2_getnext(device_ip, community, "1.3.6.1.2.1.2.2.1.16", port=161))
    print(get_ifs(device_ip, 'Router', community))
    print(get_ifs(nexus_ip, 'switch', community))
    print(get_ifs(asa_ip, 'ASA', community))
