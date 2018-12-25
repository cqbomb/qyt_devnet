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
def device_config_dev(request, devname):  # 特定设备的设备配置页面
    # 从Devicedb数据库表获取所有的设备信息
    result = Devicedb.objects.all()
    devices_list = []
    # 产生包含所有设备名称的列表devices_list
    for x in result:
        devices_list.append(x.name)

    try:
        devicename = devname
        # 提取特定设备的配置备份, 按照时间倒序
        deviceconfig = Deviceconfig.objects.filter(name=devicename).order_by('-date')

        device_config_date_hash = []
        tzutc_8 = timezone(timedelta(hours=8))  # 设置时区为东八区
        for x in deviceconfig:
            # 读取特定设备的所有配置备份信息, 制作一个字典, 然后逐个添加到device_config_date_hash列表中
            device_config_date_hash.append(
                {'name': devicename,  # 设备名称
                 'hash': x.hash,  # 配置MD5值
                 'date': x.date.astimezone(tzutc_8).strftime('%Y-%m-%d %H:%M'),  # 配置备份时间
                 'id': x.id,  # 配置唯一ID
                 'delete_url': '/deviceconfig/delete/' + devicename + '/' + str(x.id),  # 删除配置链接
                 'show_url': '/deviceconfig/show/' + devicename + '/' + str(x.id),  # 查看配置链接
                 'download_url': '/deviceconfig/download/' + devicename + '/' + str(+ x.id)})  # 下载配置链接
        # 返回device_config.html页面, 与相应数据
        return render(request, 'device_config.html', {'devices_list': devices_list,  # 设备名称清单
                                                      'current': devicename,  # 特定设备名称
                                                      # 当前设备配置备份清单
                                                      'device_config_date_hash': device_config_date_hash})
    except Exception:
        # 如果出现问题, 返回device_config.html页面
        return render(request, 'device_config.html')


@login_required()
def device_show_config(request, devname, id):  # 查看特定设备, 特定ID配置备份页面
    # 从数据库Deviceconfig中获取特定设备,特定ID的配置
    deviceconfig = Deviceconfig.objects.get(name=devname, id=id)
    # 设置时区为东八区
    tzutc_8 = timezone(timedelta(hours=8))
    # 返回show_config.html页面
    return render(request, 'show_config.html', {'devicename': devname,  # 设备名称
                                                # 备份配置日期
                                                'date': deviceconfig.date.astimezone(tzutc_8).strftime('%Y-%m-%d %H:%M'),
                                                # 配置内容
                                                'config': deviceconfig.config})


@login_required()
def device_del_config(request, devname, id):  # 删除特定设备, 特定ID配置
    # 从数据库Deviceconfig删除特定设备, 特定ID配置 条目
    m = Deviceconfig.objects.get(name=devname, id=id)
    m.delete()
    # 删除后, 重定向到查看特定设备备份配置页面
    return HttpResponseRedirect('/deviceconfig/' + devname)


@login_required()
def device_download_config(request, devname, id):
    # 获取特定设备, 特定ID配置备份
    deviceconfig = Deviceconfig.objects.get(name=devname, id=id)
    # 设置时区为东八区
    tzutc_8 = timezone(timedelta(hours=8))
    # 拼接产生下载文件的文件名(设备名称 + 备份日期 + .txt)
    filename = devname + ' ' + deviceconfig.date.astimezone(tzutc_8).strftime('%Y-%m-%d %H:%M') + '.txt'
    # 由于下载系统为win!所以需要替换linux的换行符\n到win的换行符'\r\n'
    content = deviceconfig.config.replace('\n', '\r\n')
    # 配置HTTP响应内容为content(文件内容), content_type='text/plain'
    response = HttpResponse(content, content_type='text/plain')
    # 在'Content-Disposition'中添加文件名
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


@login_required()
def device_config_compare(request, devname, id1, id2):
    # 获取特定设备的配置1
    deviceconfig1 = Deviceconfig.objects.get(name=devname, id=id1)
    # 使用'\r\n'或者'\n'分割设备配置1成为列表, ASA的配置使用'\r\n', 其它使用'\n'
    config1_list = re.split('\r\n|\n', deviceconfig1.config)
    # 获取特定设备的配置2
    deviceconfig2 = Deviceconfig.objects.get(name=devname, id=id2)
    # 使用'\r\n'或者'\n'分割设备配置2成为列表, ASA的配置使用'\r\n', 其它使用'\n'
    config2_list = re.split('\r\n|\n', deviceconfig2.config)
    # 使用Python内置的Differ()进行对比, 不用导入模块(这个部分困惑了我一阵子)
    result = Differ().compare(config1_list, config2_list)

    # 把比较的结果恢复到正常的文本
    compare_result = '\r\n'.join(list(result))
    # 返回compare_config.html页面
    return render(request, 'compare_config.html', {'devicename': devname, 'id1': id1, 'id2': id2, 'compare_result': compare_result})

