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


def getlifetime():  # 获取Netflow与Devicestatus数据的老化时间
    result_device_status = LifetimeDevicestatus.objects.get(id=1)  # 获取Devicestatus数据的老化时间
    result_netflow = LifetimeNetflow.objects.get(id=1)  # 获取Netflow数据的老化时间
    # 返回Netflow与Devicestatus数据的老化时间
    return result_device_status.lifetime, result_netflow.lifetime


def getinterval():  # 获取所有监控周期
    cpu_interval = Devicemonitorintervalcpu.objects.get(id=1).cpu_interval  # 获取CPU利用率监控周期
    mem_interval = Devicemonitorintervalmem.objects.get(id=1).mem_interval  # 获取内存利用率监控周期
    speed_interval = Devicemonitorintervalspeed.objects.get(id=1).speed_interval  # 获取接口速率监控周期
    utilization_interval = Devicemonitorintervalutilization.objects.get(id=1).utilization_interval  # 获取接口利用率监控周期
    # 返回所有监控周期
    return cpu_interval, mem_interval, speed_interval, utilization_interval


def getnetflow():  # 获取Netflow相关参数
    result_netflow_interval = Netflowinterval.objects.get(id=1).netflow_interval  # 获取Netflow监控周期
    result_netflow_lifetime= LifetimeNetflow.objects.get(id=1).lifetime  # 获取Netflow数据老化时间
    # 返回Netflow相关参数
    return result_netflow_interval, result_netflow_lifetime


def getthreshold_mail():  # 获取监控阈值与邮箱相关设置
    # 由于监控阈值与邮件相关设置是可选项, 所以需要判断是否已经设置了相关参数, 如果没有返回空""
    # 获取CPU监控阈值与告警周期
    try:
        result_thresholdcpu = Thresholdcpu.objects.get(id=1)
        cpu_threshold = result_thresholdcpu.cpu_threshold
        cpu_alarm_interval = result_thresholdcpu.alarm_interval
    except Exception:
        cpu_threshold = ""
        cpu_alarm_interval = ""
    # 获取内存监控阈值与告警周期
    try:
        result_thresholdmem = Thresholdmem.objects.get(id=1)
        mem_threshold = result_thresholdmem.mem_threshold
        mem_alarm_interval = result_thresholdmem.alarm_interval
    except Exception:
        mem_threshold = ''
        mem_alarm_interval = ''
    # 获取接口利用率监控阈值与告警周期
    try:
        result_thresholdutilization = Thresholdutilization.objects.get(id=1)
        utilization_threshold = result_thresholdutilization.utilization_threshold
        utilization_alarm_interval = result_thresholdutilization.alarm_interval
    except Exception:
        utilization_threshold = ''
        utilization_alarm_interval = ''
    # 获取邮箱相关设置
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
    # 返回监控阈值与邮箱相关设置
    return cpu_threshold, cpu_alarm_interval, mem_threshold, mem_alarm_interval, utilization_threshold, utilization_alarm_interval, mailserver, mailusername, mailpassword, mailfrom, mailto


@login_required()
def sysconfig_lifetime(request):  # 系统设置, 数据老化时间
    # 首先获取各种数据老化时间
    lifetime = getlifetime()
    # Devicestatus老化时间
    devicestatus_lifetime = lifetime[0]
    # Netflow老化时间
    netflow_lifetime = lifetime[1]

    if request.method == 'POST':
        form = SysconfiglifetimeForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把客户提交的老化时间写入数据库
        if form.is_valid():
            result_device_status = LifetimeDevicestatus.objects.get(id=1)
            result_netflow = LifetimeNetflow.objects.get(id=1)
            result_device_status.lifetime = request.POST.get('devicestatus_lifetime')
            result_netflow.lifetime = request.POST.get('netflow_lifetime')

            result_device_status.save()
            result_netflow.save()
            # 写入成功后,重定向返回到系统设置 老化时间的设置页面
            return HttpResponseRedirect('/sysconfig/lifetime')
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            return render(request, 'sysconfig_lifetime.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 把老化时间在数据库中的值,通过初始值的方式展现给客户看
        form = SysconfiglifetimeForm(initial={'devicestatus_lifetime': devicestatus_lifetime,  # initial填写初始值
                                              'netflow_lifetime': netflow_lifetime})
        # 返回'sysconfig_lifetime.html'页面,与表单给客户
        return render(request, 'sysconfig_lifetime.html', {'form': form})


@login_required()
def sysconfig_reset_lifetime(request):  # 重置老化时间
    if request.method == 'POST':  # 如果收到客户重置老化时间的POST请求
        result_device_status = LifetimeDevicestatus.objects.get(id=1)
        result_netflow = LifetimeNetflow.objects.get(id=1)
        # 重置Devicestatus老化时间到默认的24小时
        result_device_status.lifetime = 24
        # 重置Netflow老化时间到默认的24小时
        result_netflow.lifetime = 24
        result_device_status.save()
        result_netflow.save()
        # 重置成功后,重定向返回到系统设置 老化时间的设置页面
        return HttpResponseRedirect('/sysconfig/lifetime')


@login_required()
def sysconfig_monitor_interval(request):  # 系统设置, 监控周期
    # 首先获取各种监控周期
    interval = getinterval()
    # CPU监控周期
    cpu_interval = interval[0]
    # 内存监控周期
    mem_interval = interval[1]
    # 接口速率监控周期
    speed_interval = interval[2]
    # 接口利用率监控周期
    utilization_interval = interval[3]

    if request.method == 'POST':
        form = SysconfigmonitorintervalForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把客户提交的监控周期写入数据库
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
            # 写入成功后,重定向返回到系统设置 监控周期的设置页面
            return HttpResponseRedirect('/sysconfig/monitor_interval')
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            return render(request, 'sysconfig_monitor_interval.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 把监控周期在数据库中的值,通过初始值的方式展现给客户看
        form = SysconfigmonitorintervalForm(initial={'cpu_interval': cpu_interval,  # initial填写初始值
                                                     'mem_interval': mem_interval,
                                                     'speed_interval': speed_interval,
                                                     'utilization_interval': utilization_interval})
        # 返回'sysconfig_monitor_interval.html'页面,与表单给客户
        return render(request, 'sysconfig_monitor_interval.html', {'form': form})


@login_required()
def sysconfig_reset_monitor_interval(request):  # 重置监控周期
    if request.method == 'POST':  # 如果收到客户重置监控周期的POST请求
        result_cpu_interval = Devicemonitorintervalcpu.objects.get(id=1)
        result_mem_interval = Devicemonitorintervalmem.objects.get(id=1)
        result_speed_interval = Devicemonitorintervalspeed.objects.get(id=1)
        result_utilization_interval = Devicemonitorintervalutilization.objects.get(id=1)

        # 重置CPU监控周期到默认的1小时
        result_cpu_interval.cpu_interval = 1
        # 重置内存监控周期到默认的1小时
        result_mem_interval.mem_interval = 1
        # 重置接口速率监控周期到默认的1小时
        result_speed_interval.speed_interval = 1
        # 重置接口利用率监控周期到默认的1小时
        result_utilization_interval.utilization_interval = 1

        result_cpu_interval.save()
        result_mem_interval.save()
        result_speed_interval.save()
        result_utilization_interval.save()
        # 重置成功后,重定向返回到系统设置 监控周期的设置页面
        return HttpResponseRedirect('/sysconfig/monitor_interval')


@login_required()
def sysconfig_netflow(request):  # 系统设置, Netflow相关参数
    # 首先获取所有Netflow相关参数
    netflow_info = getnetflow()
    # Netflow监控周期
    netflow_interval = netflow_info[0]
    # Netflow数据老化时间
    netflow_lifetime = netflow_info[1]

    if request.method == 'POST':
        form = SysconfignetflowForm(request.POST)
        # 如果请求为POST,并且Form校验通过,把客户提交的Netflow相关参数写入数据库
        if form.is_valid():
            result_netflow_interval = Netflowinterval.objects.get(id=1)
            result_netflow_lifetime = LifetimeNetflow.objects.get(id=1)
            result_netflow_interval.netflow_interval = request.POST.get('netflow_interval')
            result_netflow_lifetime.lifetime = request.POST.get('netflow_lifetime')

            result_netflow_interval.save()
            result_netflow_lifetime.save()
            # 写入成功后,重定向返回到系统设置 Netflow相关参数的设置页面
            return HttpResponseRedirect('/sysconfig/netflow')
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            return render(request, 'sysconfig_netflow.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 把Netflow相关参数在数据库中的值,通过初始值的方式展现给客户看
        form = SysconfignetflowForm(initial={'netflow_interval': netflow_interval,  # initial填写初始值
                                             'netflow_lifetime': netflow_lifetime})
        # 返回'sysconfig_netflow.html'页面,与表单给客户
        return render(request, 'sysconfig_netflow.html', {'form': form})


@login_required()
def sysconfig_reset_netflow(request):  # 重置Netflow相关参数
    if request.method == 'POST':  # 如果收到客户重置Netflow相关参数的POST请求
        result_netflow_interval = Netflowinterval.objects.get(id=1)
        result_netflow_lifetime = LifetimeNetflow.objects.get(id=1)
        # 重置Netflow监控周期到默认的1小时
        result_netflow_interval.netflow_interval = 1
        # 重置Netflow数据老化时间到默认的24小时
        result_netflow_lifetime.lifetime = 24

        result_netflow_interval.save()
        result_netflow_lifetime.save()
        # 重置成功后,重定向返回到系统设置 Netflow相关参数的设置页面
        return HttpResponseRedirect('/sysconfig/netflow')


@login_required()
def sysconfig_reset_netflow_db(request):  # 清空Netflow数据库
    if request.method == 'POST':  # 如果收到客户清空Netflow数据库的POST请求
        Netflow.objects.all().delete()  # 删除Netflow数据库所有记录
        # 清空Netflow数据库后,重定向返回到系统设置 Netflow相关参数的设置页面
        return HttpResponseRedirect('/sysconfig/netflow')


@login_required()
def sysconfig_threshold_mail(request):  # 系统设置, 监控阈值与邮件通知
    # 获取所有监控阈值与邮件通知
    threshold_mail_info = getthreshold_mail()

    # CPU监控阈值
    cpu_threshold = threshold_mail_info[0]
    # CPU告警周期
    cpu_alarm_interval = threshold_mail_info[1]
    # 内存监控阈值
    mem_threshold = threshold_mail_info[2]
    # 内存告警周期
    mem_alarm_interval = threshold_mail_info[3]
    # 接口利用率监控阈值
    utilization_threshold = threshold_mail_info[4]
    # 接口利用率告警周期
    utilization_alarm_interval = threshold_mail_info[5]

    # 邮件服务器
    mailserver = threshold_mail_info[6]
    # 邮件服务器登录用户名
    mailusername = threshold_mail_info[7]
    # 邮件服务器登录密码
    mailpassword = threshold_mail_info[8]
    # 发件人
    mailfrom = threshold_mail_info[9]
    # 收件人
    mailto = threshold_mail_info[10]
    if request.method == 'POST':
        form = Sysconfigthreshold(request.POST)
        # 如果请求为POST,并且Form校验通过,把客户提交的监控阈值与邮件通知信息写入数据库
        if form.is_valid():
            # 写入CPU告警阈值与告警周期, 并且把当前时间写入到最近一次告警时间
            S1 = Thresholdcpu(id=1,
                              cpu_threshold=request.POST.get('cpu_threshold'),
                              alarm_interval=request.POST.get('cpu_alarm_interval'),
                              last_alarm_time=datetime.now())
            S1.save()
            # 写入内存告警阈值与告警周期, 并且把当前时间写入到最近一次告警时间
            S2 = Thresholdmem(id=1,
                              mem_threshold=request.POST.get('mem_threshold'),
                              alarm_interval=request.POST.get('mem_alarm_interval'),
                              last_alarm_time=datetime.now())
            S2.save()
            # 写入接口利用率告警阈值与告警周期, 并且把当前时间写入到最近一次告警时间
            S3 = Thresholdutilization(id=1,
                                      utilization_threshold=request.POST.get('utilization_threshold'),
                                      alarm_interval=request.POST.get('utilization_alarm_interval'),
                                      last_alarm_time=datetime.now())
            S3.save()
            # 只有邮件相关内容全部填写后, 才写入数据库
            if request.POST.get('mailserver') and request.POST.get('mailusername') and request.POST.get('mailpassword') and request.POST.get('mailfrom') and request.POST.get('mailto'):
                S4 = Smtplogindb(id=1,
                                 mailserver=request.POST.get('mailserver'),
                                 mailusername=request.POST.get('mailusername'),
                                 mailpassword=request.POST.get('mailpassword'),
                                 mailfrom=request.POST.get('mailfrom'),
                                 mailto=request.POST.get('mailto'))
                S4.save()

            # 写入成功后,重定向返回到系统设置 监控阈值与邮件通知的设置页面
            return HttpResponseRedirect('/sysconfig/threshold_mail')
        else:  # 如果Form校验失败,返回客户在Form中输入的内容和报错信息
            return render(request, 'sysconfig_threshold_mail.html', {'form': form})
    else:  # 如果不是POST,就是GET,表示为初始访问, 把监控阈值与邮件通知在数据库中的值,通过初始值的方式展现给客户看
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
        # 返回'sysconfig_threshold_mail.html'页面,与表单给客户
        return render(request, 'sysconfig_threshold_mail.html', {'form': form})


@login_required()
def sysconfig_reset_threshold_mail(request):  # 重置监控阈值与邮件通知
    if request.method == 'POST':  # 如果收到客户重置监控阈值与邮件通知的POST请求
        # 删除所有 监控阈值与邮件通知 相关设置
        Thresholdcpu.objects.all().delete()
        Thresholdmem.objects.all().delete()
        Thresholdutilization.objects.all().delete()
        Smtplogindb.objects.all().delete()

        # 写入成功后,重定向返回到系统设置 监控阈值与邮件通知的设置页面
        return HttpResponseRedirect('/sysconfig/threshold_mail')

