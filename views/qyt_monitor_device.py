#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from qytdb.models import Devicedb, Device_reachable, Devicecpumem, Deviceinterfaces, Devicestatus, Deviceinterfaces_utilization
from qytdb.models import Devicemonitorintervalcpu, Devicemonitorintervalmem, Devicemonitorintervalspeed, Devicemonitorintervalutilization
from django.shortcuts import render
from datetime import datetime, timedelta, timezone
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def getinterval_cpu():
    # 获取CPU监控周期
    result = Devicemonitorintervalcpu.objects.all()
    if len(result) == 0:
        # 如果没有条目, 设置初始化CPU监控周期为一个小时
        d1 = Devicemonitorintervalcpu(id=1,
                                      cpu_interval=1)
        d1.save()
        interval = 1  # 返回CPU监控周期为一个小时
    else:  # 如果有!获取数据库中设置的CPU监控周期
        interval = Devicemonitorintervalcpu.objects.get(id=1).cpu_interval
    # 返回CPU监控周期
    return interval


def getinterval_mem():
    # 获取内存监控周期
    result = Devicemonitorintervalmem.objects.all()
    if len(result) == 0:
        # 如果没有条目, 设置初始化内存监控周期为一个小时
        d1 = Devicemonitorintervalmem(id=1,
                                      mem_interval=1)
        d1.save()
        interval = 1  # 返回内存监控周期为一个小时
    else:  # 如果有!获取数据库中设置的内存监控周期
        interval = Devicemonitorintervalmem.objects.get(id=1).mem_interval
    # 返回内存监控周期
    return interval


def getinterval_speed():
    # 获取接口速率监控周期
    result = Devicemonitorintervalspeed.objects.all()
    if len(result) == 0:
        # 如果没有条目, 设置接口速率监控周期为一个小时
        d1 = Devicemonitorintervalspeed(id=1,
                                        speed_interval=1)
        d1.save()
        interval = 1  # 返回接口速率监控周期为一个小时
    else:  # 如果有!获取数据库中设置的接口速率监控周期
        interval = Devicemonitorintervalspeed.objects.get(id=1).speed_interval
    # 返回接口速率监控周期
    return interval


def getinterval_utilization():
    # 获取接口利用率监控周期
    result = Devicemonitorintervalutilization.objects.all()
    print(result)
    if len(result) == 0:
        # 如果没有条目, 设置接口利用率监控周期为一个小时
        d1 = Devicemonitorintervalutilization(id=1,
                                              utilization_interval=1)
        d1.save()
        interval = 1  # 返回接口利用率监控周期为一个小时
    else:  # 如果有!获取数据库中设置的接口利用率监控周期
        interval = Devicemonitorintervalutilization.objects.get(id=1).utilization_interval
    # 返回接口利用率监控周期
    return interval


def get_device_if_speed_info(devicename="default"):  # 获取设备接口速率信息
    # 获取所有设备信息
    result = Devicedb.objects.all()
    devices_list = []
    # 产生包含设备名称的清单
    for x in result:
        devices_list.append(x.name)
    try:
        if devicename == 'default':  # 如果设备名称为"default"
            devicename = devices_list[0]  # 设备名称使用设备清单里边的第一个设备名称

        # 提取特定设备,在接口速率监控周期内的信息
        if_speed = Deviceinterfaces_utilization.objects.filter(name=devicename,
                                                               date__gte=datetime.now() - timedelta(hours=getinterval_speed()))
        # 提取特定设备的接口名称清单
        ifs_name = Deviceinterfaces.objects.get(name=devicename)

        if_speed_rx_data = []
        if_speed_tx_data = []
        if_speed_time = []

        tzutc_8 = timezone(timedelta(hours=8))  # 设置时区为东八区
        for x in if_speed:
            try:
                # 提取每一分钟采集的入向接口速率信息,放入清单if_speed_rx_data,由于存入的时候使用JSON格式,所以需要用json.loads转换为Python对象
                if_speed_rx_data.append(json.loads(x.interfaces_current_speed_rx))
                # 提取每一分钟采集的出向接口速率信息,放入清单if_speed_tx_data,由于存入的时候使用JSON格式,所以需要用json.loads转换为Python对象
                if_speed_tx_data.append(json.loads(x.interfaces_current_speed_tx))
                # 提取采集时间,转换格式,然后放入清单if_speed_time
                if_speed_time.append(x.date.astimezone(tzutc_8).strftime('%H:%M'))
            except Exception:
                continue
        speed_rx_data_list = []
        # 老方案
        # for name in json.loads(ifs_name.interfaces):  # 循环得到每一个接口名字
        #     name_speed_rx_list = []
        #     for x in if_speed_rx_data:
        #         # print(x) [['Outside', 0.51], ['Inside', 0.66], ['MGMT', 7.15]]
        #         for y in x:
        #             # ping(y) ['Outside', 0.51]
        #             if y[0] == name:  # 找到匹配接口的数据,并把它放入清单
        #                 name_speed_rx_list.append(y[1])
        #     # 最终得到 [名字, 接口入向速率清单, 记录时间的清单]
        # speed_rx_data_list.append([name, name_speed_rx_list, if_speed_time])
        # speed_rx_data_list最终形态如下
        # [['Outside',[0.44, 0.47, ...],['12:40', '12:41', ...]], ['Inside', [0.44, 0.47, ...],['12:40', '12:41', ...]], ...]

        # 新方案
        for i in range(len(if_speed_rx_data[0])):  # 得到接口个数
            if_name = if_speed_rx_data[0][i][0]  # 提取接口名称
            if_result = []
            for x in if_speed_rx_data:  # x为[['Outside', 0.44], ['Inside', 0.66], ['MGMT', 7.04]]
                if_result.append(x[i][1])  # [i][0] 为具体的数据
            speed_rx_data_list.append([if_name, if_result, if_speed_time])
        # speed_rx_data_list最终形态如下
        # [['Outside',[0.44, 0.47, ...],['12:40', '12:41', ...]], ['Inside', [0.44, 0.47, ...],['12:40', '12:41', ...]], ...]

        """
        期待有更好的数据处理方案来处理得到name_speed_rx_list
        [['Outside', 0.44], ['Inside', 0.66], ['MGMT', 7.04]]
        [['Outside', 0.44], ['Inside', 0.66], ['MGMT', 10.35]]
        [['Outside', 0.45], ['Inside', 0.67], ['MGMT', 7.17]]
        [['Outside', 0.47], ['Inside', 0.63], ['MGMT', 7.16]]
        [['Outside', 0.44], ['Inside', 0.65], ['MGMT', 6.68]]
        [['Outside', 0.41], ['Inside', 0.63], ['MGMT', 7.01]]
        [['Outside', 1.28], ['Inside', 0.95], ['MGMT', 6.96]]
        [['Outside', 0.44], ['Inside', 0.65], ['MGMT', 7.2]]
        [['Outside', 0.37], ['Inside', 0.64], ['MGMT', 6.85]]
        [['Outside', 0.39], ['Inside', 0.59], ['MGMT', 7.3]]
        
        name_speed_rx_list为如下清单
        [0.39, 0.43, 0.43, 0.57, 0.42, 0.48, 1.23, 0.43, 0.5, 0.36, 1.15, 0.51, 0.5, 0.37, 0.49, 0.37, 0.46, 0.38, 0.51, 0.39, 0.45, 0.69, 1.32, 0.51, 0.62, 0.36, 0.36, 0.51, 1.47, 0.33, 0.48, 0.39, 0.43, 1.18, 0.41, 0.43, 0.51, 0.46, 0.43, 0.41, 0.6, 0.58, 1.26, 0.43, 0.44, 0.44, 0.45, 0.47, 0.44, 0.41, 1.28, 0.44, 0.37, 0.39, 0.51, 0.32, 0.48, 0.39, 0.44, 0.35]
        """

        speed_tx_data_list = []
        # for name in json.loads(ifs_name.interfaces):  # 循环得到每一个接口名字
        #     name_speed_tx_list = []
        #     for x in if_speed_tx_data:
        #         for y in x:
        #             if y[0] == name:  # 找到匹配接口的数据,并把它放入清单
        #                 name_speed_tx_list.append(y[1])
        #     speed_tx_data_list.append([name, name_speed_tx_list, if_speed_time])
        # 最终返回, 设备名称清单, 特定设备接口清单, 特定设备入向速率清单, 特定设备出向速率清单

        # 新方案
        for i in range(len(if_speed_tx_data[0])):  # 得到接口个数
            if_name = if_speed_tx_data[0][i][0]  # 提取接口名称
            if_result = []
            for x in if_speed_tx_data:  # x为[['Outside', 0.44], ['Inside', 0.66], ['MGMT', 7.04]]
                if_result.append(x[i][1])  # [i][0] 为具体的数据
            speed_tx_data_list.append([if_name, if_result, if_speed_time])

        return devices_list, json.loads(ifs_name.interfaces), speed_rx_data_list, speed_tx_data_list
    except Exception:
        return None


def get_device_if_utilization_info(devicename="default"):
    # 获取所有设备信息
    result = Devicedb.objects.all()
    devices_list = []
    # 产生包含设备名称的清单
    for x in result:
        devices_list.append(x.name)
    try:
        if devicename == 'default':  # 如果设备名称为"default"
            devicename = devices_list[0]  # 设备名称使用设备清单里边的第一个设备名称

        # 提取特定设备,在接口利用率监控周期内的信息
        if_utilization = Deviceinterfaces_utilization.objects.filter(name=devicename,
                                                                     date__gte=datetime.now() - timedelta(hours=getinterval_utilization()))
        # 提取特定设备的接口名称清单
        ifs_name = Deviceinterfaces.objects.get(name=devicename)

        if_utilization_rx_data = []
        if_utilization_tx_data = []
        if_utilization_time = []

        tzutc_8 = timezone(timedelta(hours=8))  # 设置时区为东八区
        for x in if_utilization:
            try:
                # 提取每一分钟采集的入向接口利用率信息,放入清单if_utilization_rx_data,由于存入的时候使用JSON格式,所以需要用json.loads转换为Python对象
                if_utilization_rx_data.append(json.loads(x.interfaces_current_utilization_rx))
                # 提取每一分钟采集的出向接口利用率信息,放入清单if_utilization_tx_data,由于存入的时候使用JSON格式,所以需要用json.loads转换为Python对象
                if_utilization_tx_data.append(json.loads(x.interfaces_current_utilization_tx))
                # 提取采集时间,转换格式,然后放入清单if_utilization_time
                if_utilization_time.append(x.date.astimezone(tzutc_8).strftime('%H:%M'))
            except Exception:
                continue

        utilization_rx_data_list = []
        # 老方案
        # for name in json.loads(ifs_name.interfaces):  # 循环得到每一个接口名字
        #     name_utilization_rx_list = []
        #     for x in if_utilization_rx_data:
        #         for y in x:
        #             if y[0] == name:  # 找到匹配接口的数据,并把它放入清单
        #                 name_utilization_rx_list.append(y[1])
        #     # 最终得到 [名字, 接口入向利用率清单, 记录时间的清单]
        #     utilization_rx_data_list.append([name, name_utilization_rx_list, if_utilization_time])

        # 新方案
        for i in range(len(if_utilization_rx_data[0])):  # 得到接口个数
            if_name = if_utilization_rx_data[0][i][0]  # 提取接口名称
            if_result = []
            for x in if_utilization_rx_data:  # x为[['Outside', 0.44], ['Inside', 0.66], ['MGMT', 7.04]]
                if_result.append(x[i][1])  # [i][0] 为具体的数据
            utilization_rx_data_list.append([if_name, if_result, if_utilization_time])

        utilization_tx_data_list = []
        # 老方案
        # for name in json.loads(ifs_name.interfaces):  # 循环得到每一个接口名字
        #     name_utilization_tx_list = []
        #     for x in if_utilization_tx_data:
        #         for y in x:
        #             if y[0] == name:  # 找到匹配接口的数据,并把它放入清单
        #                 name_utilization_tx_list.append(y[1])
        #     # 最终得到 [名字, 接口出向利用率清单, 记录时间的清单]
        #     utilization_tx_data_list.append([name, name_utilization_tx_list, if_utilization_time])
        # 最终返回, 设备名称清单, 特定设备接口清单, 特定设备入向利用率清单, 特定设备出向利用率清单

        # 新方案
        for i in range(len(if_utilization_tx_data[0])):  # 得到接口个数
            if_name = if_utilization_tx_data[0][i][0]  # 提取接口名称
            if_result = []
            for x in if_utilization_tx_data:  # x为[['Outside', 0.44], ['Inside', 0.66], ['MGMT', 7.04]]
                if_result.append(x[i][1])  # [i][0] 为具体的数据
            utilization_tx_data_list.append([if_name, if_result, if_utilization_time])

        return devices_list, json.loads(ifs_name.interfaces), utilization_rx_data_list, utilization_tx_data_list
    except Exception:
        return None


@login_required()
def monitor_cpu(request):  # 监控CPU利用率默认页面
    # 获取所有设备信息
    result = Devicedb.objects.all()
    devices_list = []
    # 产生包含设备名称的清单
    for x in result:
        devices_list.append(x.name)

    try:
        devicename = devices_list[0]  # 由于是默认页面, 所以显示设备清单中第一个设备的信息
        # 获取特定设备,在CPU监控周期内采集到的CPU利用率信息,按照时间排序
        cpus = Devicestatus.objects.order_by('date').filter(name=devicename, date__gte=datetime.now() - timedelta(hours=getinterval_cpu()))

        cpu_data = []
        cpu_time = []
        tzutc_8 = timezone(timedelta(hours=8))  # 设置时区为东八区
        for x in cpus:
            cpu_data.append(x.cpu)  # 把每一分钟采集到的CPU利用率写入cpu_data清单
            # 把采集时间格式化然后写入cpu_time清单
            cpu_time.append(x.date.astimezone(tzutc_8).strftime('%H:%M'))
        # 返回'monitor_devices_cpu.html'页面,与设备清单, 当前设备, CPU利用率清单cpu_data, CPU采集时间清单cpu_time
        # 由于数据会被JavaScript使用, 所以需要使用JSON转换为字符串
        return render(request, 'monitor_devices_cpu.html', {'devices_list': devices_list, 'current': devicename, 'cpu_data': json.dumps(cpu_data), 'cpu_time': json.dumps(cpu_time)})

    except Exception:
        return render(request, 'monitor_devices_cpu.html')


@login_required()
def monitor_cpu_dev(request, devicename):  # 监控特定设备CPU利用率页面
    # 获取所有设备信息
    result = Devicedb.objects.all()
    devices_list = []
    # 产生包含设备名称的清单
    for x in result:
        devices_list.append(x.name)
    # 获取特定设备,在CPU监控周期内采集到的CPU利用率信息,按照时间排序
    cpus = Devicestatus.objects.order_by('date').filter(name=devicename, date__gte=datetime.now() - timedelta(hours=getinterval_cpu()))

    cpu_data = []
    cpu_time = []
    tzutc_8 = timezone(timedelta(hours=8))  # 设置时区为东八区
    for x in cpus:
        cpu_data.append(x.cpu)  # 把每一分钟采集到的CPU利用率写入cpu_data清单
        # 把采集时间格式化然后写入cpu_time清单
        cpu_time.append(x.date.astimezone(tzutc_8).strftime('%H:%M'))
    # 返回'monitor_devices_cpu.html'页面,与设备清单, 当前设备, CPU利用率清单cpu_data, CPU采集时间清单cpu_time
    # 由于数据会被JavaScript使用, 所以需要使用JSON转换为字符串
    return render(request, 'monitor_devices_cpu.html', {'devices_list': devices_list, 'current': devicename, 'cpu_data': json.dumps(cpu_data), 'cpu_time': json.dumps(cpu_time)})


@login_required()
def monitor_mem(request):  # 监控内存利用率默认页面
    # 获取所有设备信息
    result = Devicedb.objects.all()
    devices_list = []
    # 产生包含设备名称的清单
    for x in result:
        devices_list.append(x.name)

    try:
        devicename = devices_list[0]  # 由于是默认页面, 所以显示设备清单中第一个设备的信息
        # 获取特定设备,在内存监控周期内采集到的内存利用率信息,按照时间排序
        mems = Devicestatus.objects.order_by('date').filter(name=devicename, date__gte=datetime.now() - timedelta(hours=getinterval_mem()))

        mem_data = []
        mem_time = []
        tzutc_8 = timezone(timedelta(hours=8))  # 设置时区为东八区
        for x in mems:
            mem_data.append(x.mem)  # 把每一分钟采集到的内存利用率写入mem_data清单
            # 把采集时间格式化然后写入mem_time清单
            mem_time.append(x.date.astimezone(tzutc_8).strftime('%H:%M'))
        # 返回'monitor_devices_mem.html'页面,与设备清单, 当前设备, 内存利用率清单mem_data, 内存采集时间清单mem_time
        # 由于数据会被JavaScript使用, 所以需要使用JSON转换为字符串
        return render(request, 'monitor_devices_mem.html', {'devices_list': devices_list, 'current': devicename, 'mem_data': json.dumps(mem_data), 'mem_time': json.dumps(mem_time)})
    except Exception:
        return render(request, 'monitor_devices_mem.html')


@login_required()
def monitor_mem_dev(request, devicename):  # 监控特定设备内存利用率页面
    # 获取所有设备信息
    result = Devicedb.objects.all()
    devices_list = []
    # 产生包含设备名称的清单
    for x in result:
        devices_list.append(x.name)
    # 获取特定设备,在内存监控周期内采集到的内存利用率信息,按照时间排序
    mems = Devicestatus.objects.order_by('date').filter(name=devicename, date__gte=datetime.now() - timedelta(hours=getinterval_mem()))

    mem_data = []
    mem_time = []
    tzutc_8 = timezone(timedelta(hours=8))  # 设置时区为东八区
    for x in mems:
        mem_data.append(x.mem)  # 把每一分钟采集到的内存利用率写入mem_data清单
        # 把采集时间格式化然后写入mem_time清单
        mem_time.append(x.date.astimezone(tzutc_8).strftime('%H:%M'))
    # 返回'monitor_devices_mem.html'页面,与设备清单, 当前设备, 内存利用率清单mem_data, 内存采集时间清单mem_time
    # 由于数据会被JavaScript使用, 所以需要使用JSON转换为字符串
    return render(request, 'monitor_devices_mem.html', {'devices_list': devices_list, 'current': devicename, 'mem_data': json.dumps(mem_data), 'mem_time': json.dumps(mem_time)})


@login_required()
def monitor_if_speed(request):  # 监控设备接口速率的默认页面
    if_data = get_device_if_speed_info("default")  # 获取默认设备的接口速率信息
    # if_data = 设备名称清单, 特定设备接口清单, 特定设备入向速率清单, 特定设备出向速率清单
    # 解决Ethernet0/0名称问题, 因为在URL中不能出现'/'
    # print(if_data)
    # (['Access_SW1', 'Access_SW2', 'Core_SW', 'ASA', 'GW'], ['mgmt0'], [['mgmt0', [6.54, 3.21, ...], ['21:46', '21:37', ...]]], [['mgmt0', [3.11, 3.11, ...], ['21:46', '21:37', ...]]])
    if if_data:
        if_list = if_data[1].copy()
        if_list_translate = [x.replace('/', '-') for x in if_list]  # 替换/为-
        # 返回'monitor_devices_if_speed.html'页面, 设备清单, 当前设备(为设备清单中第一个设备), 接口列表(转换后), 接口名称(选择菜单的第一个接口名称, 所以用清单中第一个接口即可),
        return render(request, 'monitor_devices_if_speed.html', {'devices_list': if_data[0],
                                                                 'current': if_data[0][0],
                                                                 'if_list': if_list_translate})
    else:
        return render(request, 'monitor_devices_if_speed.html')


@login_required()
def monitor_if_speed_dev(request, devicename):  # 监控特定设备接口速率的页面
    if_data = get_device_if_speed_info(devicename)  # 获取特定设备的接口速率信息
    # if_data = 设备名称清单, 特定设备接口清单, 特定设备入向速率清单, 特定设备出向速率清单
    # 解决Ethernet0/0名称问题, 因为在URL中不能出现'/'
    # print(if_data)
    # (['Access_SW1', 'Access_SW2', 'Core_SW', 'ASA', 'GW'], ['mgmt0'], [['mgmt0', [6.54, 3.21, ...], ['21:46', '21:37', ...]]], [['mgmt0', [3.11, 3.11, ...], ['21:46', '21:37', ...]]])
    if_list = if_data[1].copy()
    if_list_translate = [x.replace('/', '-') for x in if_list]  # 替换/为-
    # 返回'monitor_devices_if_speed.html'页面, 设备清单, 当前设备名称, 接口列表(转换后), 接口名称(选择菜单的第一个接口名称, 所以用清单中第一个接口即可),
    return render(request, 'monitor_devices_if_speed.html', {'devices_list': if_data[0],
                                                             'current': devicename,
                                                             'if_list': if_list_translate})


@login_required()
def monitor_if_speed_dev_if_direc(request, devicename, ifname, direction):  # 为特定设备,特定接口,特定方向 接口速率 线形图提供JSON数据
    if_data = get_device_if_speed_info(devicename)  # 获取特定设备的接口速率信息
    if direction == 'rx':  # 如果方向为入向
        for rx_data in if_data[2]:  # 提取入向速率信息
            if rx_data[0] == ifname.replace('-', '/'):  # 找到特定接口入向速率信息
                # 返回接口名称, 入向数据列表, 记录时间列表
                return JsonResponse({"ifname": rx_data[0], "speed_data": rx_data[1], "speed_time": rx_data[2]})
    elif direction == 'tx':  # 如果方向为出向
        for tx_data in if_data[3]:  # 提取出向速率信息
            if tx_data[0] == ifname.replace('-', '/'):  # 找到特定接口出向速率信息
                # 返回接口名称, 出向数据列表, 记录时间列表
                return JsonResponse({"ifname": tx_data[0], "speed_data": tx_data[1], "speed_time": tx_data[2]})


@login_required()
def monitor_if_utilization(request):  # 监控设备接口利用率的默认页面
    if_data = get_device_if_utilization_info("default")  # 获取默认设备的接口利用率信息
    # if_data = 设备名称清单, 特定设备接口清单, 特定设备入向利用率清单, 特定设备出向利用率清单
    # 解决Ethernet0/0名称问题, 因为在URL中不能出现'/'
    if if_data:
        if_list = if_data[1].copy()
        if_list_translate = [x.replace('/', '-') for x in if_list]  # 替换/为-
        # 返回'monitor_devices_if_utilization.html'页面, 设备清单, 当前设备(为设备清单中第一个设备), 接口列表(转换后), 接口名称(选择菜单的第一个接口名称, 所以用清单中第一个接口即可),
        return render(request, 'monitor_devices_if_utilization.html', {'devices_list': if_data[0],
                                                                       'current': if_data[0][0],
                                                                       'if_list': if_list_translate})
    else:
        return render(request, 'monitor_devices_if_utilization.html')


@login_required()
def monitor_if_utilization_dev(request, devicename):  # 监控特定设备接口利用率的页面
    if_data = get_device_if_utilization_info(devicename)  # 获取特定设备的接口利用率信息
    # if_data = 设备名称清单, 特定设备接口清单, 特定设备入向利用率清单, 特定设备出向利用率清单
    # 解决Ethernet0/0名称问题, 因为在URL中不能出现'/'
    if_list = if_data[1].copy()
    if_list_translate = [x.replace('/', '-') for x in if_list]  # 替换/为-
    # 返回'monitor_devices_if_utilization.html'页面, 设备清单, 当前设备名称, 接口列表(转换后), 接口名称(选择菜单的第一个接口名称, 所以用清单中第一个接口即可),
    return render(request, 'monitor_devices_if_utilization.html', {'devices_list': if_data[0],
                                                                   'current': devicename,
                                                                   'if_list': if_list_translate})


@login_required()
def monitor_if_utilization_dev_if_direc(request, devicename, ifname, direction):  # 为特定设备,特定接口,特定方向 接口利用率 线形图提供JSON数据
    if_data = get_device_if_utilization_info(devicename)  # 获取特定设备的接口利用率信息
    if direction == 'rx':  # 如果方向为入向
        for rx_data in if_data[2]:  # 提取入向利用率信息
            if rx_data[0] == ifname.replace('-', '/'):  # 找到特定接口入向利用率信息
                # 返回接口名称, 入向数据列表, 记录时间列表
                return JsonResponse({"ifname": rx_data[0], "utilization_data": rx_data[1], "utilization_time": rx_data[2]})
    elif direction == 'tx':  # 如果方向为出向
        for tx_data in if_data[3]:  # 提取出向利用率信息
            if tx_data[0] == ifname.replace('-', '/'):  # 找到特定接口出向利用率信息
                # 返回接口名称, 出向数据列表, 记录时间列表
                return JsonResponse({"ifname": tx_data[0], "utilization_data": tx_data[1], "utilization_time": tx_data[2]})
