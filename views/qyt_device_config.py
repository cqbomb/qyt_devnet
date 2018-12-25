#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from qytdb.models import Deviceconfig, Devicedb
from django.shortcuts import render
from datetime import datetime, timedelta, timezone
from django.http import HttpResponseRedirect, HttpResponse
from difflib import *
from django.contrib.auth.decorators import login_required
import re


@login_required()
def device_config(request):  # 设备配置默认页面
    # 从Devicedb数据库表获取所有的设备信息
    result = Devicedb.objects.all()
    devices_list = []
    # 产生包含所有设备名称的列表devices_list
    for x in result:
        devices_list.append(x.name)
    try:
        devicename = devices_list[0]  # 由于是设备配置的默认页面,所以我们找到设备清单中的第一个设备
        # 在Deviceconfig中找到第一个设备的配置信息,按照时间倒序排序
        deviceconfig = Deviceconfig.objects.filter(name=devicename).order_by('-date')

        device_config_date_hash = []
        tzutc_8 = timezone(timedelta(hours=8))  # 设置时区为东八区
        for x in deviceconfig:
            # 读取第一个设备的所有配置备份信息, 制作一个字典, 然后逐个添加到device_config_date_hash列表中
            device_config_date_hash.append({'name': devicename,  # 设备名称
                                            'hash': x.hash,  # 配置MD5值
                                            'id': x.id,  # 配置唯一ID
                                            # 配置备份时间
                                            'date': x.date.astimezone(tzutc_8).strftime('%Y-%m-%d %H:%M'),
                                            # 删除配置链接
                                            'delete_url': '/deviceconfig/delete/' + devicename + '/' + str(x.id),
                                            # 查看配置链接
                                            'show_url': '/deviceconfig/show/' + devicename + '/' + str(x.id),
                                            # 下载配置链接
                                            'download_url': '/deviceconfig/download/' + devicename + '/' + str(+ x.id)})
        # 返回device_config.html页面, 与相应数据
        return render(request, 'device_config.html', {'devices_list': devices_list,  # 设备名称清单
                                                      'current': devicename,  # 第一个设备名称
                                                      # 当前设备配置备份清单
                                                      'device_config_date_hash': device_config_date_hash})

    except Exception:
        # 如果出现问题, 返回device_config.html页面
        return render(request, 'device_config.html')


@login_required()
def device_config_dev(request, devname):
    result = Devicedb.objects.all()
    devices_list = []
    for x in result:
        devices_list.append(x.name)
    # print(devices_list)
    try:
        devicename = devname
        # print(devicename)
        deviceconfig = Deviceconfig.objects.filter(name=devicename).order_by('-date')

        device_config_date_hash = []
        tzutc_8 = timezone(timedelta(hours=8))
        for x in deviceconfig:
            # print(x)
            device_config_date_hash.append(
                {'name': devicename,
                 'hash': x.hash,
                 'date': x.date.astimezone(tzutc_8).strftime('%Y-%m-%d %H:%M'),
                 'id': x.id,
                 'delete_url': '/deviceconfig/delete/' + devicename + '/' + str(x.id),
                 'show_url': '/deviceconfig/show/' + devicename + '/' + str(x.id),
                 'download_url': '/deviceconfig/download/' + devicename + '/' + str(+ x.id)})
        # print(device_config_date_hash)
        return render(request, 'device_config.html', {'devices_list': devices_list, 'current': devicename,
                                                      'device_config_date_hash': device_config_date_hash})

    except Exception as e:
        print(e)
        return render(request, 'device_config.html')


@login_required()
def device_show_config(request, devname, id):
    deviceconfig = Deviceconfig.objects.get(name=devname, id=id)
    # print(deviceconfig)
    tzutc_8 = timezone(timedelta(hours=8))
    return render(request, 'show_config.html', {'devicename': devname,
                                                'date': deviceconfig.date.astimezone(tzutc_8).strftime('%Y-%m-%d %H:%M'),
                                                'config': deviceconfig.config})


@login_required()
def device_del_config(request, devname, id):
    m = Deviceconfig.objects.filter(name=devname, id=id)
    for x in m:
        x.delete()

    return HttpResponseRedirect('/deviceconfig/' + devname)


@login_required()
def device_download_config(request, devname, id):
    deviceconfig = Deviceconfig.objects.get(name=devname, id=id)
    tzutc_8 = timezone(timedelta(hours=8))
    filename = devname + ' ' + deviceconfig.date.astimezone(tzutc_8).strftime('%Y-%m-%d %H:%M') + '.txt'
    content = deviceconfig.config.replace('\n', '\r\n')
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


@login_required()
def device_config_compare(request, devname, id1, id2):
    deviceconfig1 = Deviceconfig.objects.get(name=devname, id=id1)
    config1_list = re.split('\r\n|\n', deviceconfig1.config)
    deviceconfig2 = Deviceconfig.objects.get(name=devname, id=id2)
    config2_list = re.split('\r\n|\n', deviceconfig2.config)
    result = Differ().compare(config1_list, config2_list)
    print(config1_list)
    print(config2_list)
    compare_result = '\r\n'.join(list(result))
    # print(compare_result)
    return render(request, 'compare_config.html', {'devicename': devname, 'id1': id1, 'id2': id2, 'compare_result': compare_result})

