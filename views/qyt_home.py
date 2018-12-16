#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from django.http import JsonResponse
from random import randint
from qytdb.models import Device_reachable, Devicecpumem

colors = ['#ff0000', '#28a745', '#333333', '#c3e6cb', '#dc3545', '#6c757d']
labels = ['安全', '数据中心', '教主VIP', '路由交换', '无线', '华为']
datas = [randint(1, 100), randint(1, 100), randint(1, 100), randint(1, 100), randint(1, 100), randint(1, 100)]


def health_reachable(request):
    result = Device_reachable.objects.all()
    green_devices = 0
    yellow_devices = 0
    red_devices = 0
    for x in result:
        if x.ssh_reachable == True and x.snmp_reachable == True:
            green_devices += 1
        elif x.ssh_reachable == False and x.snmp_reachable == False:
            red_devices += 1
        else:
            yellow_devices += 1
    colors = ['#228b22', '#ffff00', '#ff0000']
    labels = ['正常', 'SNMP或SSH不可达', '全部不可达']
    datas = [green_devices, yellow_devices, red_devices]
    return JsonResponse({'colors': colors, 'labels': labels, 'datas': datas})


def health_cpu(request):
    result = Devicecpumem.objects.all()
    green_devices = 0
    yellow_devices = 0
    red_devices = 0
    for x in result:
        if x.cpu_current_utilization >= 70:
            red_devices += 1
        elif 70 > x.cpu_current_utilization >= 30:
            yellow_devices += 1
        else:
            green_devices += 1
    colors = ['#228b22', '#ffff00', '#ff0000']
    labels = ['低于30%', '30%到70%之间', '高于70%']
    datas = [green_devices, yellow_devices, red_devices]
    return JsonResponse({'colors': colors, 'labels': labels, 'datas': datas})


def health_mem(request):
    result = Devicecpumem.objects.all()
    green_devices = 0
    yellow_devices = 0
    red_devices = 0
    for x in result:
        if x.mem_current_utilization >= 70:
            red_devices += 1
        elif 70 > x.mem_current_utilization >= 30:
            yellow_devices += 1
        else:
            green_devices += 1
    colors = ['#228b22', '#ffff00', '#ff0000']
    labels = ['低于30%', '30%到70%之间', '高于70%']
    datas = [green_devices, yellow_devices, red_devices]
    return JsonResponse({'colors': colors, 'labels': labels, 'datas': datas})

