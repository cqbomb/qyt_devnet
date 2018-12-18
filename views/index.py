#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from django.shortcuts import render
from qytdb.models import Devicecpumem, Deviceinterfaces_utilization, Devicedb


def index(request):
    devices_cpu_list = []
    devices_mem_list = []
    result = Devicecpumem.objects.order_by("-cpu_max_utilization")
    i = 1
    for x in result:
        if i <= 3:
            devices_cpu_list.append({'name': x.name, 'cpu_max': x.cpu_max_utilization, 'cpu_current': x.cpu_current_utilization})
            devices_mem_list.append({'name': x.name, 'mem_max': x.mem_max_utilization, 'mem_current': x.mem_current_utilization})
            i += 1
        else:
            break
    device_result = Devicedb.objects.all()
    device_name_list = [device.name for device in device_result]
    if_utilization_rx = []
    if_utilization_tx = []
    for device in device_name_list:
        utilization_result = Deviceinterfaces_utilization.objects.filter(name=device).last()
        print(utilization_result.name)
        print(utilization_result.interfaces_max_utilization_rx)
        print(utilization_result.interfaces_max_utilization_tx)
    return render(request, 'index.html', {'devices_cpu_list': devices_cpu_list, 'devices_mem_list': devices_mem_list})
