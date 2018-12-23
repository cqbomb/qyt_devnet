#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from django.shortcuts import render
from qytdb.models import LifetimeNetflow, LifetimeDevicestatus
from qytdb.models import Devicemonitorintervalcpu, Devicemonitorintervalmem, Devicemonitorintervalspeed, Devicemonitorintervalutilization
from qytdb.forms import SysconfiglifetimeForm, SysconfigmonitorintervalForm, SysconfignetflowForm, Sysconfigthreshold
from qytdb.models import Smtplogindb
from qytdb.models import Netflowinterval
from qytdb.models import Thresholdutilization, Thresholdcpu, Thresholdmem
from django.http import HttpResponseRedirect


def getlifetime():
    result_device_status = LifetimeDevicestatus.objects.get(id=1)
    result_netflow = LifetimeNetflow.objects.get(id=1)

    return result_device_status.lifetime, result_netflow.lifetime


def getinterval():
    cpu_interval = Devicemonitorintervalcpu.objects.get(id=1).cpu_interval
    mem_interval = Devicemonitorintervalmem.objects.get(id=1).mem_interval
    speed_interval = Devicemonitorintervalspeed.objects.get(id=1).speed_interval
    utilization_interval = Devicemonitorintervalutilization.objects.get(id=1).utilization_interval

    return cpu_interval, mem_interval, speed_interval, utilization_interval


def getnetflow():
    result_netflow_interval = Netflowinterval.objects.get(id=1).netflow_interval
    result_netflow_lifetime= LifetimeNetflow.objects.get(id=1).lifetime

    return result_netflow_interval, result_netflow_lifetime


def getthreshold_mail():
    result_thresholdcpu = Thresholdcpu.objects.get(id=1)
    result_thresholdmem = Thresholdmem.objects.get(id=1)
    result_thresholdutilization = Thresholdutilization.objects.get(id=1)
    result_smtplogindb = Smtplogindb.objects.get(id=1)
    cpu_threshold = result_thresholdcpu.cpu_threshold
    cpu_alarm_interval = result_thresholdcpu.alarm_interval
    mem_threshold = result_thresholdmem.mem_threshold
    mem_alarm_interval = result_thresholdmem.alarm_interval
    utilization_threshold = result_thresholdutilization.utilization_threshold
    utilization_alarm_interval = result_thresholdutilization.alarm_interval
    mailserver = result_smtplogindb.mailserver
    mailusername = result_smtplogindb.mailusername
    mailpassword = result_smtplogindb.mailpassword
    mailfrom = result_smtplogindb.mailfrom
    mailto = result_smtplogindb.mailto
    return cpu_threshold, cpu_alarm_interval, mem_threshold, mem_alarm_interval, utilization_threshold, utilization_alarm_interval, mailserver, mailusername, mailpassword, mailfrom, mailto


def sysconfig_lifetime(request):
    # 首先获取特定ID学员详细信息
    lifetime = getlifetime()
    devicestatus_lifetime = lifetime[0]
    netflow_lifetime = lifetime[1]

    if request.method == 'POST':
        form = SysconfiglifetimeForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把修改过的设备信息写入数据库
        if form.is_valid():
            result_device_status = LifetimeDevicestatus.objects.get(id=1)
            result_netflow = LifetimeNetflow.objects.get(id=1)
            result_device_status.lifetime = request.POST.get('devicestatus_lifetime')
            result_netflow.lifetime = request.POST.get('netflow_lifetime')

            result_device_status.save()
            result_netflow.save()
            # 写入成功后,重定向返回展示所有学员信息的页面
            return HttpResponseRedirect('/sysconfig/lifetime')
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            return render(request, 'sysconfig_lifetime.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 把特定ID客户在数据库中的值,通过初始值的方式展现给客户看
        form = SysconfiglifetimeForm(initial={'devicestatus_lifetime': devicestatus_lifetime,  # initial填写初始值
                                              'netflow_lifetime': netflow_lifetime})
        return render(request, 'sysconfig_lifetime.html', {'form': form})


def sysconfig_monitor_interval(request):
    # 首先获取特定ID学员详细信息
    interval = getinterval()
    cpu_interval = interval[0]
    mem_interval = interval[1]
    speed_interval = interval[2]
    utilization_interval = interval[3]

    if request.method == 'POST':
        form = SysconfigmonitorintervalForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把修改过的设备信息写入数据库
        if form.is_valid():
            result_cpu_interval = Devicemonitorintervalcpu.objects.get(id=1)
            result_mem_interval = Devicemonitorintervalmem.objects.get(id=1)
            result_speed_interval = Devicemonitorintervalspeed.objects.get(id=1)
            result_utilization_interval = Devicemonitorintervalutilization.objects.get(id=1)

            result_cpu_interval.cpu_interval = request.POST.get('cpu_interval')
            result_mem_interval.mem_interval = request.POST.get('mem_interval')
            result_speed_interval.speed_interval = request.POST.get('speed_interval')
            result_utilization_interval.utilization_interval = request.POST.get('utilization_interval')

            result_cpu_interval.save()
            result_mem_interval.save()
            result_speed_interval.save()
            result_utilization_interval.save()
            # 写入成功后,重定向返回展示所有学员信息的页面
            return HttpResponseRedirect('/sysconfig/monitor_interval')
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            return render(request, 'sysconfig_monitor_interval.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 把特定ID客户在数据库中的值,通过初始值的方式展现给客户看
        form = SysconfigmonitorintervalForm(initial={'cpu_interval': cpu_interval,  # initial填写初始值
                                                     'mem_interval': mem_interval,
                                                     'speed_interval': speed_interval,
                                                     'utilization_interval': utilization_interval})
        return render(request, 'sysconfig_monitor_interval.html', {'form': form})


def sysconfig_netflow(request):
    # 首先获取特定ID学员详细信息
    netflow_info = getnetflow()
    netflow_interval = netflow_info[0]
    netflow_lifetime = netflow_info[1]

    if request.method == 'POST':
        form = SysconfignetflowForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把修改过的设备信息写入数据库
        if form.is_valid():
            result_netflow_interval = Netflowinterval.objects.get(id=1)
            result_netflow_lifetime = LifetimeNetflow.objects.get(id=1)
            result_netflow_interval.netflow_interval = request.POST.get('netflow_interval')
            result_netflow_lifetime.lifetime = request.POST.get('netflow_lifetime')

            result_netflow_interval.save()
            result_netflow_lifetime.save()
            # 写入成功后,重定向返回展示所有学员信息的页面
            return HttpResponseRedirect('/sysconfig/netflow')
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            return render(request, 'sysconfig_netflow.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 把特定ID客户在数据库中的值,通过初始值的方式展现给客户看
        form = SysconfignetflowForm(initial={'netflow_interval': netflow_interval,  # initial填写初始值
                                             'netflow_lifetime': netflow_lifetime})
        return render(request, 'sysconfig_netflow.html', {'form': form})


def sysconfig_threshold_mail(request):
    threshold_mail_info = getthreshold_mail()

    cpu_threshold = threshold_mail_info[0]
    cpu_alarm_interval = threshold_mail_info[1]

    mem_threshold = threshold_mail_info[2]
    mem_alarm_interval = threshold_mail_info[3]

    utilization_threshold = threshold_mail_info[4]
    utilization_alarm_interval = threshold_mail_info[5]

    mailserver = threshold_mail_info[6]
    mailusername = threshold_mail_info[7]
    mailpassword = threshold_mail_info[8]
    mailfrom = threshold_mail_info[9]
    mailto = threshold_mail_info[10]
    if request.method == 'POST':
        form = Sysconfigthreshold(request.POST)
        # 如果请求为POST,并且Form校验通过,把修改过的设备信息写入数据库
        if form.is_valid():
            result_thresholdcpu = Thresholdcpu.objects.get(id=1)
            result_thresholdmem = Thresholdmem.objects.get(id=1)
            result_thresholdutilization = Thresholdutilization.objects.get(id=1)
            result_smtplogindb = Smtplogindb.objects.get(id=1)

            result_thresholdcpu.cpu_threshold = request.POST.get('cpu_threshold')
            result_thresholdcpu.alarm_interval = request.POST.get('cpu_alarm_interval')

            result_thresholdmem.mem_threshold = request.POST.get('mem_threshold')
            result_thresholdmem.alarm_interval = request.POST.get('mem_alarm_interval')

            result_thresholdutilization.utilization_threshold = request.POST.get('utilization_threshold')
            result_thresholdutilization.alarm_interval = request.POST.get('utilization_alarm_interval')

            result_smtplogindb.mailserver = request.POST.get('mailserver')
            result_smtplogindb.mailusername = request.POST.get('mailusername')
            result_smtplogindb.mailpassword = request.POST.get('mailpassword')
            result_smtplogindb.mailfrom = request.POST.get('mailfrom')
            result_smtplogindb.mailto = request.POST.get('mailto')

            result_thresholdcpu.save()
            result_thresholdmem.save()
            result_thresholdutilization.save()
            result_smtplogindb.save()

            # 写入成功后,重定向返回展示所有学员信息的页面
            return HttpResponseRedirect('/sysconfig/threshold_mail')
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            return render(request, 'sysconfig_threshold_mail.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 把特定ID客户在数据库中的值,通过初始值的方式展现给客户看
        form = Sysconfigthreshold(initial={"cpu_threshold": cpu_threshold,
                                           "cpu_alarm_interval": cpu_alarm_interval,
                                           "mem_threshold":mem_threshold,
                                           "mem_alarm_interval": mem_alarm_interval,
                                           "utilization_threshold": utilization_threshold,
                                           "utilization_alarm_interval": utilization_alarm_interval,
                                           "mailserver": mailserver,
                                           "mailusername": mailusername,
                                           "mailpassword": mailpassword,
                                           "mailfrom": mailfrom,
                                           "mailto": mailto})

        return render(request, 'sysconfig_threshold_mail.html', {'form': form})



