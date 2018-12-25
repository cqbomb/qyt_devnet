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


# 首页处理views
def index(request):
    devices_cpu_list = []
    # 最大CPU利用率排倒序,order_by("-cpu_max_utilization")
    cpu_result = Devicecpumem.objects.order_by("-cpu_max_utilization")
    i = 1
    # 得到前三的最大CPU利用率的设备信息
    for x in cpu_result:
        if i <= 3:
            devices_cpu_list.append({'name': x.name, 'cpu_max': x.cpu_max_utilization, 'cpu_current': x.cpu_current_utilization})
            i += 1
        else:
            break

    devices_mem_list = []
    # 最大内存利用率排倒序,order_by("-mem_max_utilization")
    mem_result = Devicecpumem.objects.order_by("-mem_max_utilization")
    i = 1
    # 得到前三的最大内存利用率的设备信息
    for x in mem_result:
        if i <= 3:
            devices_mem_list.append({'name': x.name, 'mem_max': x.mem_max_utilization, 'mem_current': x.mem_current_utilization})
            i += 1
        else:
            break
    # 查询设备数据库
    device_result = Devicedb.objects.all()
    # 得到所有设备名称的清单
    device_name_list = [device.name for device in device_result]
    if_utilization_rx = []
    if_utilization_tx = []
    for device in device_name_list:
        try:
            # 获取设备最近一次接口利用率记录
            utilization_result = Deviceinterfaces_utilization.objects.filter(name=device).last()
            # 设备入向最大利用率放入u_rx_list清单
            u_rx_list = json.loads(utilization_result.interfaces_max_utilization_rx)
            # 设备入向当前利用率放入u_c_rx_list清单
            u_c_rx_list = json.loads(utilization_result.interfaces_current_utilization_rx)
            # 设备出向最大利用率放入u_tx_list清单
            u_tx_list = json.loads(utilization_result.interfaces_max_utilization_tx)
            # 设备出向当前利用率放入u_c_tx_list清单
            u_c_tx_list = json.loads(utilization_result.interfaces_current_utilization_tx)
            u_if_rx_list = []
            u_if_tx_list = []
            for x in zip(u_rx_list, u_c_rx_list):
                # x 为 (['Ethernet0/0', 0.07], ['Ethernet0/0', 0.03])
                # u_if_rx_list 条目为 [设备名称, 接口名称, 入向最大利用率, 入向当前利用率]
                u_if_rx_list.append([device, x[0][0], x[0][1], x[1][1]])
            for x in zip(u_tx_list, u_c_tx_list):
                u_if_tx_list.append([device, x[0][0], x[0][1], x[1][1]])
            # 扩展if_utilization_rx, 所以if_utilization_rx为[[设备名称, 接口名称, 入向最大利用率, 入向当前利用率],...]
            if_utilization_rx.extend(u_if_rx_list)
            if_utilization_tx.extend(u_if_tx_list)
        except Exception:
            continue
    # if_utilization_rx的格式为[[设备名称, 接口名称, 入向最大利用率, 入向当前利用率],...]
    # 使用sorted + lambda技术进行排序, 排序的键值为入向最大利用率x[2], reverse=True为反向排序, [0:3]取前三(Top 3)
    top_3_if_utilization_rx = sorted(if_utilization_rx, key=lambda x: x[2], reverse=True)[0:3]
    # 从top_3_if_utilization_rx中提取设备名称x[0], 接口名称x[1], 入向最大利用率x[2], 入向当前利用率x[3], 写入字典再放入列表
    # top_3_if_utilization_rx_dict为一个列表, 里边的对象是字典
    top_3_if_utilization_rx_dict = [{'name': x[0], 'ifname': x[1], 'rx_max': x[2], 'rx_current': x[3]} for x in top_3_if_utilization_rx]

    top_3_if_utilization_tx = sorted(if_utilization_tx, key=lambda x: x[2], reverse=True)[0:3]
    top_3_if_utilization_tx_dict = [{'name': x[0], 'ifname': x[1], 'tx_max': x[2], 'tx_current': x[3]} for x in top_3_if_utilization_tx]

    # 返回页面为index.html
    # devices_cpu_list为Top3 的CPU利用率
    # devices_mem_list为Top3 的内存利用率
    # top_3_if_utilization_rx_dict为Top3 的入向接口利用率
    # top_3_if_utilization_tx_dict为Top3 的出向接口利用率
    return render(request, 'index.html', {'devices_cpu_list': devices_cpu_list,
                                          'devices_mem_list': devices_mem_list,
                                          'top_3_if_utilization_rx_dict': top_3_if_utilization_rx_dict,
                                          'top_3_if_utilization_tx_dict': top_3_if_utilization_tx_dict})
