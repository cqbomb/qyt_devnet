#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from qytdb.models import DevicetypeSNMP
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def show_devicetypes(request):
    # 查询整个DevicetypeSNMP数据库信息 object.all()
    result = DevicetypeSNMP.objects.all()
    # 最终得到设备类型清单devicetype_lis,清单内部是每一个设备信息的字典
    devicetypes_list = []
    for x in result:
        # 产生设备信息的字典
        devicetypes_dict = {}
        # 设备类型
        devicetypes_dict['type'] = x.type
        # 设备类型名称
        devicetypes_dict['type_name'] = x.type_name
        # CPU利用率OID
        devicetypes_dict['cpu_oid'] = x.cpu_oid
        # 使用内存OID
        devicetypes_dict['mem_used_oid'] = x.mem_used_oid
        # 闲置内存OID
        devicetypes_dict['mem_free_oid'] = x.mem_free_oid
        # 接口名称清单OID
        devicetypes_dict['interfaces_name_oid'] = x.interfaces_name_oid
        # 接口带宽清单OID
        devicetypes_dict['interfaces_bw_oid'] = x.interfaces_bw_oid
        # 接口入向字节数清单OID
        devicetypes_dict['interfaces_in_bytes_oid'] = x.interfaces_in_bytes_oid
        # 接口出向字节数清单OID
        devicetypes_dict['interfaces_out_bytes_oid'] = x.interfaces_out_bytes_oid

        devicetypes_list.append(devicetypes_dict)
    # 返回'show_devicetypes.html'页面, 与包含所有设备信息字典的devicetypes_list清单
    return render(request, 'show_devicetypes.html', {'devicetypes_list': devicetypes_list})
