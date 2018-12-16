#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from qytdb.models import Devicedb, Device_reachable, Devicecpumem, Deviceinterfaces, Devicestatus, Deviceinterfaces_utilization
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
    result = Devicedb.objects.all()
    devices_list = []
    for x in result:
        devices_list.append(x.name)

    mems = Devicestatus.objects.filter(name=devices_list[0], date__gte=datetime.now() - timedelta(hours=1))

    mem_data = []
    mem_time = []
    tzutc_8 = timezone(timedelta(hours=8))
    for x in mems:
        mem_data.append(x.mem)
        mem_time.append(x.date.astimezone(tzutc_8).strftime('%H:%M'))

    return render(request, 'monitor_devices_mem.html', {'devices_list': devices_list, 'current': devices_list[0], 'mem_data': json.dumps(mem_data), 'mem_time': json.dumps(mem_time)})


def monitor_mem_dev(request, devicename):
    result = Devicedb.objects.all()
    devices_list = []
    for x in result:
        devices_list.append(x.name)

    mems = Devicestatus.objects.filter(name=devicename, date__gte=datetime.now() - timedelta(hours=1))

    mem_data = []
    mem_time = []
    tzutc_8 = timezone(timedelta(hours=8))
    for x in mems:
        mem_data.append(x.mem)
        mem_time.append(x.date.astimezone(tzutc_8).strftime('%H:%M'))

    return render(request, 'monitor_devices_mem.html', {'devices_list': devices_list, 'current': devicename, 'mem_data': json.dumps(mem_data), 'mem_time': json.dumps(mem_time)})


def monitor_if_speed(request):
    result = Devicedb.objects.all()
    devices_list = []
    for x in result:
        devices_list.append(x.name)

    if_speed = Deviceinterfaces_utilization.objects.filter(name=devices_list[0], date__gte=datetime.now() - timedelta(hours=1))
    ifs_name = Deviceinterfaces.objects.get(name=devices_list[0])

    if_speed_rx_data = []
    if_speed_tx_data = []
    if_speed_time = []

    tzutc_8 = timezone(timedelta(hours=8))
    for x in if_speed:
        if_speed_rx_data.append(json.loads(x.interfaces_current_speed_rx))
        if_speed_tx_data.append(json.loads(x.interfaces_current_speed_tx))
        if_speed_time.append(x.date.astimezone(tzutc_8).strftime('%H:%M'))

    speed_rx_data_list = []
    for name in json.loads(ifs_name.interfaces):  # 循环得到每一个接口名字
        name_speed_rx_list = []
        for x in if_speed_rx_data:
            for y in x:
                if y[0] == name:  # 找到匹配接口的数据,并把它放入清单
                    name_speed_rx_list.append(round(y[1]/1000, 2))  # 控制浮点数的境地
        speed_rx_data_list.append([name, name_speed_rx_list, if_speed_time])

    speed_tx_data_list = []
    for name in json.loads(ifs_name.interfaces):  # 循环得到每一个接口名字
        name_speed_tx_list = []
        for x in if_speed_tx_data:
            for y in x:
                if y[0] == name:  # 找到匹配接口的数据,并把它放入清单
                    name_speed_tx_list.append(round(y[1]/1000, 2))  # 控制浮点数的境地
        speed_tx_data_list.append([name, name_speed_tx_list, if_speed_time])

    return render(request, 'monitor_devices_if_speed.html', {'devices_list': devices_list, 'current': devices_list[0], 'if_list': json.loads(ifs_name.interfaces), 'speed_rx_data_list': json.dumps(speed_rx_data_list), 'speed_tx_data_list': json.dumps(speed_tx_data_list)})


def monitor_if_speed_dev(request, devicename):
    result = Devicedb.objects.all()
    devices_list = []
    for x in result:
        devices_list.append(x.name)

    if_speed = Deviceinterfaces_utilization.objects.filter(name=devicename, date__gte=datetime.now() - timedelta(hours=1))
    ifs_name = Deviceinterfaces.objects.get(name=devicename)

    if_speed_rx_data = []
    if_speed_tx_data = []
    if_speed_time = []

    tzutc_8 = timezone(timedelta(hours=8))
    for x in if_speed:
        if_speed_rx_data.append(json.loads(x.interfaces_current_speed_rx))
        if_speed_tx_data.append(json.loads(x.interfaces_current_speed_tx))
        if_speed_time.append(x.date.astimezone(tzutc_8).strftime('%H:%M'))

    speed_rx_data_list = []
    for name in json.loads(ifs_name.interfaces):  # 循环得到每一个接口名字
        name_speed_rx_list = []
        for x in if_speed_rx_data:
            for y in x:
                if y[0] == name:  # 找到匹配接口的数据,并把它放入清单
                    name_speed_rx_list.append(round(y[1]/1000, 2))  # 控制浮点数的境地
        speed_rx_data_list.append([name, name_speed_rx_list, if_speed_time])

    speed_tx_data_list = []
    for name in json.loads(ifs_name.interfaces):  # 循环得到每一个接口名字
        name_speed_tx_list = []
        for x in if_speed_tx_data:
            for y in x:
                if y[0] == name:  # 找到匹配接口的数据,并把它放入清单
                    name_speed_tx_list.append(round(y[1]/1000, 2))  # 控制浮点数的境地
        speed_tx_data_list.append([name, name_speed_tx_list, if_speed_time])

    return render(request, 'monitor_devices_if_speed.html', {'devices_list': devices_list, 'current': devicename, 'if_list': json.loads(ifs_name.interfaces), 'speed_rx_data_list': json.dumps(speed_rx_data_list), 'speed_tx_data_list': json.dumps(speed_tx_data_list)})


def monitor_if_utilization(request):
    return render(request, 'monitor_devices_if_utilization.html')


def monitor_if_utilization_dev(request):
    return render(request, 'monitor_devices_if_utilization.html')

