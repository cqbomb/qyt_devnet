#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名"})
                               )
    password = forms.CharField(label='密码',
                               max_length=100,
                               required=True,
                               widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "密码"})
                               )

