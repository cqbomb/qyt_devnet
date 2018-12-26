#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from qytdb.models import Devicedb, Device_reachable, Devicecpumem, Deviceinterfaces
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def show_devices(request):
    # 查询整个Devicedb数据库信息 object.all()
    result = Devicedb.objects.all()
    # 最终得到设备清单devices_lis,清单内部是每一个设备信息的字典
    devices_list = []
    for x in result:
        # 产生设备信息的字典
        devices_dict = {}
        # 为了不在模板中拼接字符串,提前为删除和编辑页面产生URI
        # 删除设备URL
        devices_dict['name_delete'] = "/deletedevice/" + str(x.name) + "/"
        # 编辑设备URL
        devices_dict['name_edit'] = "/editdevice/" + str(x.name) + "/"
        # 设备名称
        devices_dict['name'] = x.name
        # 设备IP地址
        devices_dict['ip'] = x.ip
        # 从数据库Device_reachable获取设备的SSH和SNMP可达性信息
        y = Device_reachable.objects.get(name=x.name)
        devices_dict['snmp_reachable'] = y.snmp_reachable
        devices_dict['ssh_reachable'] = y.ssh_reachable
        # 从数据库Devicecpumem获取设备的CPU和内存利用率信息
        z = Devicecpumem.objects.get(name=x.name)
        devices_dict['cpu_max'] = z.cpu_max_utilization
        devices_dict['cpu_current'] = z.cpu_current_utilization
        devices_dict['mem_max'] = z.mem_max_utilization
        devices_dict['mem_current'] = z.mem_current_utilization
        # 从数据库Deviceinterfaces获取设备接口数量信息
        ifs = Deviceinterfaces.objects.get(name=x.name)
        devices_dict['ifs'] = ifs.interfaces_num
        # 把设备信息添加到字典,再添加到devices_list清单
        devices_list.append(devices_dict)
    # 返回'show_devices.html'页面, 与包含所有设备信息字典的devices_list清单
    return render(request, 'show_devices.html', {'devices_list': devices_list})