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
from django.http import HttpResponseRedirect


def del_device(request, devicename):
    m = Devicedb.objects.get(name=devicename)
    m.delete()
    m = Device_reachable.objects.get(name=devicename)
    m.delete()
    m = Devicecpumem.objects.get(name=devicename)
    m.delete()
    m = Deviceinterfaces.objects.get(name=devicename)
    m.delete()
    m = Devicestatus.objects.filter(name=devicename)
    for x in m:
        x.delete()
    m = Deviceconfig.objects.filter(name=devicename)
    for x in m:
        x.delete()
    return HttpResponseRedirect('/showdevices/')


if __name__ == '__main__':
    pass
