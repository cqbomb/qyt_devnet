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
from qytdb.models import Deviceconfig
from django.http import HttpResponseRedirect
from django.shortcuts import render
from qytdb.forms import DeviceForm
from modules.qyt_devnet_6_get_device_config_md5 import get_config_md5_from_device
from django.contrib.auth.decorators import login_required


@login_required()
def add_devices(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把新添加的设备信息写入数据库
        if form.is_valid():
            # 把设备信息写入Devicedb数据库
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
            # 在Devicecpumem表中创建条目,Devicecpumem不会随着时间的增加而增加
            d2 = Devicecpumem(name=request.POST.get('name'))
            d2.save()
            # 在Deviceinterfaces表中创建条目,Deviceinterfaces不会随着时间的增加而增加
            d3 = Deviceinterfaces(name=request.POST.get('name'))
            d3.save()
            # 在Device_reachable表中创建条目,Device_reachable不会随着时间的增加而增加
            d4 = Device_reachable(name=request.POST.get('name'))
            d4.save()
            # 在Deviceinterfaces_utilization表中创建条目,Deviceinterfaces_utilization不会随着时间的增加而增加
            d5 = Deviceinterfaces_utilization(name=request.POST.get('name'))
            d5.save()

            # 从Devicedb表中读回设备信息
            device = Devicedb.objects.get(name=request.POST.get('name'))

            # 由于enable密码不是必填内容,所以需要判断一下是否有enable密码
            # 下面的操作是为了设备做一次初始化备份
            if device.enable_password:
                config, md5 = get_config_md5_from_device(device.ip, device.ssh_username, device.ssh_password, device.type, device.enable_password)
            else:
                config, md5 = get_config_md5_from_device(device.ip, device.ssh_username, device.ssh_password, device.type)
            # 把获取的设备配置与MD5值,存入Deviceconfig数据库表
            d6 = Deviceconfig(name=request.POST.get('name'),
                              hash=md5,
                              config=config)
            d6.save()

            # 写入成功后,重定向返回展示所有设备信息的页面
            return HttpResponseRedirect('/showdevices/')
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            # 如果检查到错误,会添加错误内容到form内,例如:<ul class="errorlist"><li>设备名不能重复</li></ul>
            return render(request, 'add_devices.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 显示表单内容给客户
        form = DeviceForm()
        return render(request, 'add_devices.html', {'form': form})
