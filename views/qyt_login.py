#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from django.shortcuts import render
from qytdb.forms import UserForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


def qyt_login(request):  # 为客户提供登录页面
    if request.method == 'POST':
        form = UserForm(request.POST)
        username = request.POST.get('username', '')  # 提取用户输入的用户名
        password = request.POST.get('password', '')  # 提取用户输入的密码
        user = authenticate(username=username, password=password)  # 产生用户认证信息
        if user is not None and user.is_active:  # 如果用户认证信息不为空,并且用户为激活状态
            login(request, user)  # 登入用户
            # 如果通过next参数指定重定向url(点击其它页面,然后重定向到登录页面,next会自动产生)
            # 就重定向到这个url,如果没有就重定向到首页
            next_url = request.GET.get('next', '/')
            return HttpResponseRedirect(next_url)

        else:  # 如果认证失败, 提示错误信息给客户
            return render(request, 'registration/login.html', {'form': form, 'error': '用户名或密码错误'})
    else:  # 如果客户使用GET访问登录页面'accounts/login/',并且客户已经认证(拥有cookie), 直接重定向到首页
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')

        else:  # 如果客户使用GET访问登录页面'accounts/login/',并且没有认证, 给客户返回登录页面'registration/login.html'
            form = UserForm()
            return render(request, 'registration/login.html', {'form': form})


def qyt_logout(request):  # 客户登出页面
    logout(request)  # 登出客户
    # 重定向客户到登录页面'/accounts/login'
    return HttpResponseRedirect('/accounts/login')
