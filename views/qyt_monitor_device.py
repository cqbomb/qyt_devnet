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
from django.http import JsonResponse


def get_device_if_speed_info(devicename="default"):

    result = Devicedb.objects.all()
    devices_list = []
    for x in result:
        devices_list.append(x.name)

    if devicename == 'default':
        devicename = devices_list[0]

    if_speed = Deviceinterfaces_utilization.objects.filter(name=devicename,
                                                           date__gte=datetime.now() - timedelta(hours=1))
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
                    name_speed_rx_list.append(round(y[1] / 1000, 2))  # 控制浮点数的境地
        speed_rx_data_list.append([name, name_speed_rx_list, if_speed_time])

    speed_tx_data_list = []
    for name in json.loads(ifs_name.interfaces):  # 循环得到每一个接口名字
        name_speed_tx_list = []
        for x in if_speed_tx_data:
            for y in x:
                if y[0] == name:  # 找到匹配接口的数据,并把它放入清单
                    name_speed_tx_list.append(round(y[1] / 1000, 2))  # 控制浮点数的境地
        speed_tx_data_list.append([name, name_speed_tx_list, if_speed_time])
    return devices_list, json.loads(ifs_name.interfaces), speed_rx_data_list, speed_tx_data_list


def get_device_if_utilization_info(devicename="default"):
    result = Devicedb.objects.all()
    devices_list = []
    for x in result:
        devices_list.append(x.name)

    if devicename == 'default':
        devicename = devices_list[0]

    if_utilization = Deviceinterfaces_utilization.objects.filter(name=devicename,
                                                           date__gte=datetime.now() - timedelta(hours=1))
    ifs_name = Deviceinterfaces.objects.get(name=devicename)

    if_utilization_rx_data = []
    if_utilization_tx_data = []
    if_utilization_time = []

    tzutc_8 = timezone(timedelta(hours=8))
    for x in if_utilization:
        if_utilization_rx_data.append(json.loads(x.interfaces_current_utilization_rx))
        if_utilization_tx_data.append(json.loads(x.interfaces_current_utilization_tx))
        if_utilization_time.append(x.date.astimezone(tzutc_8).strftime('%H:%M'))

    utilization_rx_data_list = []
    for name in json.loads(ifs_name.interfaces):  # 循环得到每一个接口名字
        name_utilization_rx_list = []
        for x in if_utilization_rx_data:
            for y in x:
                if y[0] == name:  # 找到匹配接口的数据,并把它放入清单
                    name_utilization_rx_list.append(y[1])  # 控制浮点数的境地
        utilization_rx_data_list.append([name, name_utilization_rx_list, if_utilization_time])

    utilization_tx_data_list = []
    for name in json.loads(ifs_name.interfaces):  # 循环得到每一个接口名字
        name_utilization_tx_list = []
        for x in if_utilization_tx_data:
            for y in x:
                if y[0] == name:  # 找到匹配接口的数据,并把它放入清单
                    name_utilization_tx_list.append(y[1])  # 控制浮点数的境地
        utilization_tx_data_list.append([name, name_utilization_tx_list, if_utilization_time])
    return devices_list, json.loads(ifs_name.interfaces), utilization_rx_data_list, utilization_tx_data_list


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
    if_data = get_device_if_speed_info("default")
    # 解决Ethernet0/0名称问题
    if_list = if_data[1].copy()
    if_list_translate = [x.replace('/', '-') for x in if_list]

    return render(request, 'monitor_devices_if_speed.html', {'devices_list': if_data[0], 'current': if_data[0][0], 'if_list': if_list_translate, 'if_name': if_data[2][0][0],  'speed_data_list': if_data[2][0][1],   'speed_time_list': if_data[2][0][2]})


def monitor_if_speed_dev(request, devicename):
    if_data = get_device_if_speed_info(devicename)
    # 解决Ethernet0/0名称问题
    if_list = if_data[1].copy()
    if_list_translate = [x.replace('/', '-') for x in if_list]

    return render(request, 'monitor_devices_if_speed.html', {'devices_list': if_data[0], 'current': devicename, 'if_list': if_list_translate, 'if_name': if_data[2][0][0],  'speed_data_list': if_data[2][0][1],   'speed_time_list': if_data[2][0][2]})


def monitor_if_speed_dev_if_direc(request, devicename, ifname, direction):
    if_data = get_device_if_speed_info(devicename)
    if direction == 'rx':
        for rx_data in if_data[2]:
            if rx_data[0] == ifname.replace('-', '/'):
                return JsonResponse({"ifname": rx_data[0], "speed_data": rx_data[1], "speed_time": rx_data[2]})
    elif direction == 'tx':
        for tx_data in if_data[3]:
            if tx_data[0] == ifname.replace('-', '/'):
                return JsonResponse({"ifname": tx_data[0], "speed_data": tx_data[1], "speed_time": tx_data[2]})


def monitor_if_utilization(request):
    if_data = get_device_if_utilization_info("default")
    # 解决Ethernet0/0名称问题
    if_list = if_data[1].copy()
    if_list_translate = [x.replace('/', '-') for x in if_list]

    return render(request, 'monitor_devices_if_utilization.html',
                  {'devices_list': if_data[0], 'current': if_data[0][0], 'if_list': if_list_translate,
                   'if_name': if_data[2][0][0], 'utilization_data_list': if_data[2][0][1],
                   'utilization_time_list': if_data[2][0][2]})


def monitor_if_utilization_dev(request, devicename):
    if_data = get_device_if_utilization_info(devicename)
    # 解决Ethernet0/0名称问题
    if_list = if_data[1].copy()
    if_list_translate = [x.replace('/', '-') for x in if_list]

    return render(request, 'monitor_devices_if_utilization.html', {'devices_list': if_data[0], 'current': devicename, 'if_list': if_list_translate, 'if_name': if_data[2][0][0],  'utilization_data_list': if_data[2][0][1],   'utilization_time_list': if_data[2][0][2]})


def monitor_if_utilization_dev_if_direc(request, devicename, ifname, direction):
    if_data = get_device_if_utilization_info(devicename)
    if direction == 'rx':
        for rx_data in if_data[2]:
            if rx_data[0] == ifname.replace('-', '/'):
                return JsonResponse({"ifname": rx_data[0], "utilization_data": rx_data[1], "utilization_time": rx_data[2]})
    elif direction == 'tx':
        for tx_data in if_data[3]:
            if tx_data[0] == ifname.replace('-', '/'):
                return JsonResponse({"ifname": tx_data[0], "utilization_data": tx_data[1], "utilization_time": tx_data[2]})