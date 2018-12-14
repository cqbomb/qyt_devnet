#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from qytdb.models import Devicedb
from qytdb.models import Devicecpumem
from qytdb.models import Device_reachable
from qytdb.models import Deviceinterfaces
from qytdb.models import Deviceinterfaces_utilization
from django.http import HttpResponseRedirect
from django.shortcuts import render
from qytdb.forms import DeviceForm


def add_devices(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把新添加的虚拟机信息写入数据库
        if form.is_valid():
            d1 = Devicedb(name=request.POST.get('name'),
                          ip=request.POST.get('ip'),
                          description=request.POST.get('description'),
                          type=request.POST.get('type'),
                          snmp_enable=request.POST.get('snmp_enable'),
                          snmp_ro_community=request.POST.get('snmp_ro_community'),
                          snmp_rw_community=request.POST.get('snmp_rw_community'),
                          ssh_username=request.POST.get('ssh_username'),
                          ssh_password=request.POST.get('ssh_password'),
                          enable_password=request.POST.get('enable_password'),)
            d1.save()
            d2 = Devicecpumem(name=request.POST.get('name'))
            d2.save()
            d3 = Deviceinterfaces(name=request.POST.get('name'))
            d3.save()
            d4 = Device_reachable(name=request.POST.get('name'))
            d4.save()
            d5 = Deviceinterfaces_utilization(name=request.POST.get('name'))
            d5.save()
            # 写入成功后,重定向返回展示所有虚拟机信息的页面
            return HttpResponseRedirect('/showdevices/')
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            # 如果检查到错误,会添加错误内容到form内,例如:<ul class="errorlist"><li>QQ号码已经存在</li></ul>
            return render(request, 'add_devices.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 显示表单内容给客户
        form = DeviceForm()
        print(form)
        print(type(form))
        return render(request, 'add_devices.html', {'form': form})
