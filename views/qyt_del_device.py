#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from qytdb.models import Devicedb
from qytdb.models import Deviceconfig
from qytdb.models import Devicecpumem
from qytdb.models import Deviceinterfaces
from qytdb.models import Devicestatus
from qytdb.models import Device_reachable
from qytdb.models import Deviceinterfaces_utilization
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


@login_required()
def del_device(request, devicename):
    # 删除Devicedb表中记录的设备信息
    m = Devicedb.objects.get(name=devicename)
    m.delete()
    # 删除Device_reachable表中记录的可达性信息
    m = Device_reachable.objects.get(name=devicename)
    m.delete()
    # 删除Devicecpumem表中记录的cpu和内存利用率的信息
    m = Devicecpumem.objects.get(name=devicename)
    m.delete()
    # 删除Deviceinterfaces表中记录的接口信息
    m = Deviceinterfaces.objects.get(name=devicename)
    m.delete()
    # 删除Deviceinterfaces_utilization表中记录的接口利用率条目,由于条目随着时间增加而增加,所以需要使用filter + for循环
    m = Deviceinterfaces_utilization.objects.filter(name=devicename)
    for x in m:
        x.delete()
    # 删除Devicestatus表中记录的设备状态条目,由于条目随着时间增加而增加,所以需要使用filter + for循环
    m = Devicestatus.objects.filter(name=devicename)
    for x in m:
        x.delete()
    # 删除Deviceconfig表中备份的设备配置条目,由于条目随着时间增加而增加,所以需要使用filter + for循环
    m = Deviceconfig.objects.filter(name=devicename)
    for x in m:
        x.delete()
    # 删除所有与设备相关条目后,重定向返回显示设备信息页面
    return HttpResponseRedirect('/showdevices/')
