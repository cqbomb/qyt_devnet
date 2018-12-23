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
from qytdb.models import Netflowinterval, Netflow
from qytdb.models import Thresholdutilization, Thresholdcpu, Thresholdmem
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

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
    try:
        result_thresholdcpu = Thresholdcpu.objects.get(id=1)
        cpu_threshold = result_thresholdcpu.cpu_threshold
        cpu_alarm_interval = result_thresholdcpu.alarm_interval
    except Exception:
        cpu_threshold = ""
        cpu_alarm_interval = ""

    try:
        result_thresholdmem = Thresholdmem.objects.get(id=1)
        mem_threshold = result_thresholdmem.mem_threshold
        mem_alarm_interval = result_thresholdmem.alarm_interval
    except Exception:
        mem_threshold = ''
        mem_alarm_interval = ''

    try:
        result_thresholdutilization = Thresholdutilization.objects.get(id=1)
        utilization_threshold = result_thresholdutilization.utilization_threshold
        utilization_alarm_interval = result_thresholdutilization.alarm_interval
    except Exception:
        utilization_threshold = ''
        utilization_alarm_interval = ''

    try:
        result_smtplogindb = Smtplogindb.objects.get(id=1)
        mailserver = result_smtplogindb.mailserver
        mailusername = result_smtplogindb.mailusername
        mailpassword = result_smtplogindb.mailpassword
        mailfrom = result_smtplogindb.mailfrom
        mailto = result_smtplogindb.mailto
    except Exception:
        mailserver = ''
        mailusername = ''
        mailpassword = ''
        mailfrom = ''
        mailto = ''
    return cpu_threshold, cpu_alarm_interval, mem_threshold, mem_alarm_interval, utilization_threshold, utilization_alarm_interval, mailserver, mailusername, mailpassword, mailfrom, mailto


@login_required()
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


@login_required()
def sysconfig_reset_lifetime(request):
    if request.method == 'POST':
        result_device_status = LifetimeDevicestatus.objects.get(id=1)
        result_netflow = LifetimeNetflow.objects.get(id=1)
        result_device_status.lifetime = 24
        result_netflow.lifetime = 24
        result_device_status.save()
        result_netflow.save()
        return HttpResponseRedirect('/sysconfig/lifetime')


@login_required()
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


@login_required()
def sysconfig_reset_monitor_interval(request):
    if request.method == 'POST':
        result_cpu_interval = Devicemonitorintervalcpu.objects.get(id=1)
        result_mem_interval = Devicemonitorintervalmem.objects.get(id=1)
        result_speed_interval = Devicemonitorintervalspeed.objects.get(id=1)
        result_utilization_interval = Devicemonitorintervalutilization.objects.get(id=1)

        result_cpu_interval.cpu_interval = 1
        result_mem_interval.mem_interval = 1
        result_speed_interval.speed_interval = 1
        result_utilization_interval.utilization_interval = 1

        result_cpu_interval.save()
        result_mem_interval.save()
        result_speed_interval.save()
        result_utilization_interval.save()
        # 写入成功后,重定向返回展示所有学员信息的页面
        return HttpResponseRedirect('/sysconfig/monitor_interval')


@login_required()
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


@login_required()
def sysconfig_reset_netflow(request):
    if request.method == 'POST':
        result_netflow_interval = Netflowinterval.objects.get(id=1)
        result_netflow_lifetime = LifetimeNetflow.objects.get(id=1)
        result_netflow_interval.netflow_interval = 1
        result_netflow_lifetime.lifetime = 24

        result_netflow_interval.save()
        result_netflow_lifetime.save()
        # 写入成功后,重定向返回展示所有学员信息的页面
        return HttpResponseRedirect('/sysconfig/netflow')


@login_required()
def sysconfig_reset_netflow_db(request):
    if request.method == 'POST':
        Netflow.objects.all().delete()
        return HttpResponseRedirect('/sysconfig/netflow')


@login_required()
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
            S1 = Thresholdcpu(id=1,
                              cpu_threshold=request.POST.get('cpu_threshold'),
                              alarm_interval=request.POST.get('cpu_alarm_interval'),
                              last_alarm_time=datetime.now())
            S1.save()

            S2 = Thresholdmem(id=1,
                              mem_threshold=request.POST.get('mem_threshold'),
                              alarm_interval=request.POST.get('mem_alarm_interval'),
                              last_alarm_time = datetime.now())
            S2.save()

            S3 = Thresholdutilization(id=1,
                                      utilization_threshold=request.POST.get('utilization_threshold'),
                                      alarm_interval=request.POST.get('utilization_alarm_interval'),
                                      last_alarm_time=datetime.now())
            S3.save()

            if request.POST.get('mailserver') and request.POST.get('mailusername') and request.POST.get('mailpassword') and request.POST.get('mailfrom') and request.POST.get('mailto'):
                S4 = Smtplogindb(id=1,
                                 mailserver=request.POST.get('mailserver'),
                                 mailusername=request.POST.get('mailusername'),
                                 mailpassword=request.POST.get('mailpassword'),
                                 mailfrom=request.POST.get('mailfrom'),
                                 mailto=request.POST.get('mailto'))
                S4.save()

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


@login_required()
def sysconfig_reset_threshold_mail(request):
    if request.method == 'POST':
        Thresholdcpu.objects.all().delete()
        Thresholdmem.objects.all().delete()
        Thresholdutilization.objects.all().delete()
        Smtplogindb.objects.all().delete()

        # 写入成功后,重定向返回展示所有学员信息的页面
        return HttpResponseRedirect('/sysconfig/threshold_mail')

