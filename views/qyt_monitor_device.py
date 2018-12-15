#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from qytdb.models import Devicedb, Device_reachable, Devicecpumem, Deviceinterfaces, Devicestatus
from django.shortcuts import render
from datetime import datetime, timedelta, timezone
import json


def monitor_cpu(request):
    result = Devicedb.objects.all()
    devices_list = []
    for x in result:
        devices_list.append(x.name)

    cpus = Devicestatus.objects.filter(name=devices_list[0], date__gte=datetime.now() - timedelta(hours=1))

    cpu_data = []
    cpu_time = []
    tzutc_8 = timezone(timedelta(hours=8))
    for x in cpus:
        cpu_data.append(x.cpu)
        cpu_time.append(x.date.astimezone(tzutc_8).strftime('%H:%M'))

    return render(request, 'monitor_devices_cpu.html', {'devices_list': devices_list, 'current': devices_list[0], 'cpu_data': json.dumps(cpu_data), 'cpu_time': json.dumps(cpu_time)})


def monitor_cpu_dev(request, devicename):
    result = Devicedb.objects.all()
    devices_list = []
    for x in result:
        devices_list.append(x.name)

    cpus = Devicestatus.objects.filter(name=devicename, date__gte=datetime.now() - timedelta(hours=1))

    cpu_data = []
    cpu_time = []
    tzutc_8 = timezone(timedelta(hours=8))
    for x in cpus:
        cpu_data.append(x.cpu)
        cpu_time.append(x.date.astimezone(tzutc_8).strftime('%H:%M'))

    return render(request, 'monitor_devices_cpu.html', {'devices_list': devices_list, 'current': devicename, 'cpu_data': json.dumps(cpu_data), 'cpu_time': json.dumps(cpu_time)})


def monitor_mem(request):
    return render(request, 'monitor_devices_mem.html')


def monitor_mem_dev(request):
    return render(request, 'monitor_devices_mem.html')


def monitor_if_speed(request):
    return render(request, 'monitor_devices_if_speed.html')


def monitor_if_speed_dev(request):
    return render(request, 'monitor_devices_if_speed.html')


def monitor_if_utilization(request):
    return render(request, 'monitor_devices_if_utilization.html')


def monitor_if_utilization_dev(request):
    return render(request, 'monitor_devices_if_utilization.html')

