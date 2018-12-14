#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from qytdb.models import Devicedb
from django.http import HttpResponseRedirect
from qytdb.forms import EditDeviceForm
from django.shortcuts import render


def getdeviceinfo(name):
    # 设置过滤条件,获取特定设备信息, objects.get(name=name)
    result = Devicedb.objects.get(name=name)
    device_dict = {}
    device_dict['name'] = result.name
    device_dict['ip'] = result.ip
    device_dict['description'] = result.description
    device_dict['type'] = result.type
    device_dict['snmp_enable'] = result.snmp_enable
    device_dict['snmp_ro_community'] = result.snmp_ro_community
    device_dict['snmp_rw_community'] = result.snmp_rw_community
    device_dict['ssh_username'] = result.ssh_username
    device_dict['ssh_password'] = result.ssh_password
    device_dict['enable_password'] = result.enable_password
    # 返回特定学员详细信息
    return device_dict


def edit_device(request, devicename):
    # 首先获取特定ID学员详细信息
    infodict = getdeviceinfo(devicename)
    if request.method == 'POST':
        form = EditDeviceForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把修改过的设备信息写入数据库
        if form.is_valid():
            m = Devicedb.objects.get(name=devicename)
            m.name = request.POST.get('name')
            m.ip = request.POST.get('ip')
            m.description = request.POST.get('description')
            m.type = request.POST.get('type')
            m.snmp_enable = request.POST.get('snmp_enable')
            m.snmp_ro_community = request.POST.get('snmp_ro_community')
            m.snmp_rw_community = request.POST.get('snmp_rw_community')
            m.ssh_username = request.POST.get('ssh_username')
            m.ssh_password = request.POST.get('ssh_password')
            m.enable_password = request.POST.get('enable_password')
            m.save()
            # 写入成功后,重定向返回展示所有学员信息的页面
            return HttpResponseRedirect('/showdevices/')
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            return render(request, 'edit_device.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 把特定ID客户在数据库中的值,通过初始值的方式展现给客户看
        form = EditDeviceForm(initial={'name': infodict['name'],  # initial填写初始值
                                       'ip': infodict['ip'],
                                       'description': infodict['description'],
                                       'type': infodict['type'],
                                       'snmp_enable': infodict['snmp_enable'],
                                       'snmp_ro_community': infodict['snmp_ro_community'],
                                       'snmp_rw_community': infodict['snmp_rw_community'],
                                       'ssh_username': infodict['ssh_username'],
                                       'ssh_password': infodict['ssh_password'],
                                       'enable_password': infodict['enable_password']
                                       })
        return render(request, 'edit_device.html', {'form': form})
