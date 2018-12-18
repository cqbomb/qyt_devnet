#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from django.shortcuts import render
from qytdb.models import Devicecpumem, Deviceinterfaces_utilization, Devicedb
import json

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
        name = utilization_result.name
        u_rx_list = json.loads(utilization_result.interfaces_max_utilization_rx)
        u_c_rx_list = json.loads(utilization_result.interfaces_current_utilization_rx)
        u_tx_list = json.loads(utilization_result.interfaces_max_utilization_tx)
        u_c_tx_list = json.loads(utilization_result.interfaces_current_utilization_tx)
        u_if_rx_list = []
        u_if_tx_list = []
        for x in zip(u_rx_list, u_c_rx_list):
            u_if_rx_list.append([name, x[0][0], x[0][1], x[1][1]])
        for x in zip(u_tx_list, u_c_tx_list):
            u_if_tx_list.append([name, x[0][0], x[0][1], x[1][1]])
        if_utilization_rx.extend(u_if_rx_list)
        if_utilization_tx.extend(u_if_tx_list)
    top_3_if_utilization_rx = sorted(if_utilization_rx, key=lambda x: x[2], reverse=True)[0:3]
    top_3_if_utilization_rx_dict = [{'name': x[0], 'ifname': x[1], 'rx_max': x[2], 'rx_current': x[3]} for x in top_3_if_utilization_rx]
    # print(top_3_if_utilization_rx_dict)
    top_3_if_utilization_tx = sorted(if_utilization_tx, key=lambda x: x[2], reverse=True)[0:3]
    top_3_if_utilization_tx_dict = [{'name': x[0], 'ifname': x[1], 'tx_max': x[2], 'tx_current': x[3]} for x in top_3_if_utilization_tx]
    # print(top_3_if_utilization_tx_dict)
    return render(request, 'index.html', {'devices_cpu_list': devices_cpu_list, 'devices_mem_list': devices_mem_list, 'top_3_if_utilization_rx_dict': top_3_if_utilization_rx_dict, 'top_3_if_utilization_tx_dict': top_3_if_utilization_tx_dict})
