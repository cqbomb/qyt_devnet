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
    # 查询整个数据库的信息 object.all()
    result = Devicedb.objects.all()
    # 最终得到学员清单students_list,清单内部是每一个学员信息的字典
    devices_list = []
    for x in result:
        # 产生学员信息的字典
        # print(x.name)
        devices_dict = {}
        # 为了不在模板中拼接字符串,提前为删除和编辑页面产生URI
        devices_dict['name_delete'] = "/deletedevice/" + str(x.name) + "/"
        devices_dict['name_edit'] = "/editdevice/" + str(x.name) + "/"

        devices_dict['name'] = x.name
        devices_dict['ip'] = x.ip
        y = Device_reachable.objects.get(name=x.name)
        devices_dict['snmp_reachable'] = y.snmp_reachable
        devices_dict['ssh_reachable'] = y.ssh_reachable
        z = Devicecpumem.objects.get(name=x.name)
        devices_dict['cpu_max'] = z.cpu_max_utilization
        devices_dict['cpu_current'] = z.cpu_current_utilization
        devices_dict['mem_max'] = z.mem_max_utilization
        devices_dict['mem_current'] = z.mem_current_utilization
        ifs = Deviceinterfaces.objects.get(name=x.name)
        devices_dict['ifs'] = ifs.interfaces_num
        devices_list.append(devices_dict)
    return render(request, 'show_devices.html', {'devices_list': devices_list})