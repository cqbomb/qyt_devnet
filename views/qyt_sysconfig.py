#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from django.shortcuts import render


def sysconfig_lifetime(request):
    return render(request, 'sysconfig_lifetime.html')


def sysconfig_monitor_interval(request):
    return render(request, 'sysconfig_monitor_interval.html')


def sysconfig_threshold_mail(request):
    return render(request, 'sysconfig_threshold_mail.html')


def sysconfig_netflow(request):
    return render(request, 'sysconfig_netflow.html')
