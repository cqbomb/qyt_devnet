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


def device_config(request):
    result = Devicedb.objects.all()
    devices_list = []
    for x in result:
        devices_list.append(x.name)
    # print(devices_list)
    try:
        devicename = devices_list[0]
        # print(devicename)
        deviceconfig = Deviceconfig.objects.filter(name=devicename).order_by('-date')

        device_config_date_hash = []
        tzutc_8 = timezone(timedelta(hours=8))
        for x in deviceconfig:
            # print(x)
            device_config_date_hash.append({'name': devicename,
                                            'hash': x.hash,
                                            'id': x.id,
                                            'date': x.date.astimezone(tzutc_8).strftime('%Y-%m-%d %H:%M'),
                                            'delete_url': '/deviceconfig/delete/' + devicename + '/' + str(x.id),
                                            'show_url': '/deviceconfig/show/' + devicename + '/' + str(x.id),
                                            'download_url': '/deviceconfig/download/' + devicename + '/' + str(+ x.id)})
        # print(device_config_date_hash)
        return render(request, 'device_config.html', {'devices_list': devices_list, 'current': devicename, 'device_config_date_hash': device_config_date_hash})

    except Exception as e:
        print(e)
        return render(request, 'device_config.html')


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


def device_show_config(request, devname, id):
    deviceconfig = Deviceconfig.objects.get(name=devname, id=id)
    # print(deviceconfig)
    tzutc_8 = timezone(timedelta(hours=8))
    return render(request, 'show_config.html', {'devicename': devname,
                                                'date': deviceconfig.date.astimezone(tzutc_8).strftime('%Y-%m-%d %H:%M'),
                                                'config': deviceconfig.config})


def device_del_config(request, devname, id):
    m = Deviceconfig.objects.filter(name=devname, id=id)
    for x in m:
        x.delete()

    return HttpResponseRedirect('/deviceconfig/' + devname)


def device_download_config(request, devname, id):
    deviceconfig = Deviceconfig.objects.get(name=devname, id=id)
    tzutc_8 = timezone(timedelta(hours=8))
    filename = devname + ' ' + deviceconfig.date.astimezone(tzutc_8).strftime('%Y-%m-%d %H:%M') + '.txt'
    content = deviceconfig.config.replace('\n', '\r\n')
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def device_config_compare(request, devname, id1, id2):
    return render(request, 'compare_config.html')

