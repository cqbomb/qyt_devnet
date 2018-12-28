#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from django import forms
from qytdb.models import Devicedb, DevicetypeSNMP
from django.core.validators import RegexValidator


# 用户登录表单
class UserForm(forms.Form):
    required_css_class = 'required'
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


# 添加设备表单
class DeviceForm(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'
    name = forms.CharField(max_length=100,
                           min_length=2,
                           label='设备名称',
                           required=True,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    # 类型为GenericIPAddressField,可以对输入的IP地址进行校验
    ip = forms.GenericIPAddressField(required=True,
                                     label='IP地址',
                                     widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="设备描述",
                                  required=False,
                                  # 输入为Textarea,支持多行输入,"rows": 3 控制展示的行数
                                  widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}))
    # 选择的设备类型
    # type_choices = [["switch", "switch22"], ["Router", "Router22"], ["ASA", "ASA22"]]
    type_choices = []
    devicetype = DevicetypeSNMP.objects.all()
    for x in devicetype:
        type_choices.append([x.type, x.type_name])
    type = forms.CharField(label='设备类型',
                           required=True,
                           widget=forms.Select(choices=type_choices,
                                               attrs={"class": "form-control"}))
    TRUE_FALSE_CHOICES = ((True, 'Yes'), (False, 'No'))
    snmp_enable = forms.ChoiceField(label='是否激活SNMP',
                                    required=True,
                                    choices=TRUE_FALSE_CHOICES,
                                    initial=False,
                                    widget=forms.Select(attrs={"class": "required checkbox form-control"}))
    community_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                     message="SNMP community 只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    snmp_ro_community = forms.CharField(max_length=100,
                                        min_length=2,
                                        label='SNMP只读',
                                        required=True,
                                        validators=[community_regex],
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    snmp_rw_community = forms.CharField(max_length=100,
                                        min_length=2,
                                        label='SNMP读写',
                                        required=False,
                                        validators=[community_regex],
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    username_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                    message="用户名只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    ssh_username = forms.CharField(max_length=100,
                                   min_length=2,
                                   label='SSH用户名',
                                   required=True,
                                   validators=[username_regex],
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    password_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                    message="密码只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    ssh_password = forms.CharField(max_length=100,
                                   min_length=2,
                                   label='SSH密码',
                                   required=True,
                                   validators=[password_regex],
                                   widget=forms.PasswordInput(attrs={"class": "form-control"}))
    enable_password_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                           message="特权密码只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    enable_password = forms.CharField(max_length=100,
                                      min_length=2,
                                      label='特权密码',
                                      required=False,
                                      validators=[enable_password_regex],
                                      widget=forms.PasswordInput(attrs={"class": "form-control"}))

    # 校验设备名称不能重复, 在此系统中,设备并没有指定唯一ID,设备名就是唯一ID,不能重复
    def clean_name(self):
        name = self.cleaned_data['name']  # 提取客户输入的设备名
        # 在数据库中查找是否存在这个设备名
        existing = Devicedb.objects.filter(
            name=name
        ).exists()
        # 如果存在就显示校验错误信息
        if existing:
            raise forms.ValidationError("设备名不能重复")
        # 如果校验成功就返回设备名
        return name

    # 校验IP地址不能重复
    def clean_ip(self):
        ip = self.cleaned_data['ip']  # 提取客户输入的设备IP
        # 在数据库中查找是否存在这个设备IP
        existing = Devicedb.objects.filter(
            ip=ip
        ).exists()
        # 如果存在就显示校验错误信息
        if existing:
            raise forms.ValidationError("设备IP不能重复")
        # 如果校验成功就返回设备IP
        return ip

    # 确认激活SNMP,才能设置只读Community
    def clean_snmp_ro_community(self):
        snmp_enable = self.cleaned_data['snmp_enable']
        snmp_ro_community = self.cleaned_data['snmp_ro_community']
        if snmp_enable == 'True' and snmp_ro_community:
            return snmp_ro_community
        else:
            raise forms.ValidationError("设置只读Community之前请激活SNMP")

    # 确认激活SNMP,才能设置读写Community
    def clean_snmp_rw_community(self):
        snmp_enable = self.cleaned_data['snmp_enable']
        snmp_rw_community = self.cleaned_data['snmp_rw_community']
        if snmp_rw_community:
            if snmp_enable == 'True' and snmp_rw_community:
                return snmp_rw_community
            else:
                raise forms.ValidationError("设置读写Community之前请激活SNMP")
        else:
            return snmp_rw_community


# 编辑设备表单
class EditDeviceForm(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'
    name = forms.CharField(max_length=100,
                           min_length=2,
                           label='设备名称(只读)',
                           required=True,
                           # 由于设备名称为唯一ID,不能修改!此处使用readonly限制客户修改
                           widget=forms.TextInput(attrs={"class": "form-control", 'readonly': True}))
    ip = forms.GenericIPAddressField(required=True,
                                     label='IP地址',
                                     widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(label="设备描述",
                                  required=False,
                                  widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}))
    type_choices = (("switch", "switch"), ("Router", "Router"), ("ASA", "ASA"))
    type = forms.CharField(label='设备类型',
                           required=True,
                           widget=forms.Select(choices=type_choices,
                                               attrs={"class": "form-control"}))
    TRUE_FALSE_CHOICES = ((True, 'Yes'), (False, 'No'))
    snmp_enable = forms.ChoiceField(label='是否激活SNMP',
                                    required=True,
                                    choices=TRUE_FALSE_CHOICES,
                                    initial=False,
                                    widget=forms.Select(attrs={"class": "required checkbox form-control"}))
    community_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                     message="SNMP community 只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    snmp_ro_community = forms.CharField(max_length=100,
                                        min_length=2,
                                        label='SNMP只读',
                                        required=True,
                                        validators=[community_regex],
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    snmp_rw_community = forms.CharField(max_length=100,
                                        min_length=2,
                                        label='SNMP读写',
                                        required=False,
                                        validators=[community_regex],
                                        widget=forms.TextInput(attrs={"class": "form-control"}))
    username_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                    message="用户名只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    ssh_username = forms.CharField(max_length=100,
                                   min_length=2,
                                   label='SSH用户名',
                                   required=True,
                                   validators=[username_regex],
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    password_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                    message="密码只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    ssh_password = forms.CharField(max_length=100,
                                   min_length=2,
                                   label='SSH密码',
                                   required=True,
                                   validators=[password_regex],
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    enable_password_regex = RegexValidator(regex=r'[0-9a-zA-Z~!@#$%^&*()_+=,./]+',
                                           message="特权密码只能包含数字,小写,大写字母 ~!@#$%^&*()_+=,./")
    enable_password = forms.CharField(max_length=100,
                                      min_length=2,
                                      label='特权密码',
                                      required=False,
                                      validators=[enable_password_regex],
                                      widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean_ip(self):
        ip = self.cleaned_data['ip']  # 提取客户输入的设备IP
        # 在数据库中查找是否存在其他设备使用这个IP地址

        for i in Devicedb.objects.filter(ip=ip):
            if i.name != self.cleaned_data['name']:
                raise forms.ValidationError("设备IP地址已经存在")
        else:
            return ip

    def clean_snmp_ro_community(self):
        snmp_enable = self.cleaned_data['snmp_enable']
        snmp_ro_community = self.cleaned_data['snmp_ro_community']
        if snmp_enable == 'True' and snmp_ro_community:
            return snmp_ro_community
        else:
            raise forms.ValidationError("设置只读Community之前请激活SNMP")

    def clean_snmp_rw_community(self):
        snmp_enable = self.cleaned_data['snmp_enable']
        snmp_rw_community = self.cleaned_data['snmp_rw_community']
        if snmp_rw_community:
            if snmp_enable == 'True' and snmp_rw_community:
                return snmp_rw_community
            else:
                raise forms.ValidationError("设置读写Community之前请激活SNMP")
        else:
            return snmp_rw_community


# 系统设置, 老化时间设置表单
class SysconfiglifetimeForm(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'
    lifetime_regex = RegexValidator(regex=r'^\d{1,5}$',
                                    message="老化时间只能支持最多5位整数")
    # 设备状态信息老化时间
    devicestatus_lifetime = forms.CharField(validators=[lifetime_regex],
                                            min_length=1,
                                            max_length=5,
                                            label='设备信息老化时间（单位小时，默认24小时）',
                                            required=True,
                                            widget=forms.NumberInput(attrs={"class": "form-control"}))
    # netflow老化时间
    netflow_lifetime = forms.CharField(validators=[lifetime_regex],
                                       min_length=1,
                                       max_length=5,
                                       label='Netflow老化时间（单位小时，默认24小时）',
                                       required=True,
                                       widget=forms.NumberInput(attrs={"class": "form-control"}))


# 系统设置, 监控周期表单
class SysconfigmonitorintervalForm(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'
    interval_regex = RegexValidator(regex=r'^\d{1,2}$',
                                    message="监控周期只能支持最多2位整数")
    # CPU监控周期
    cpu_interval = forms.CharField(validators=[interval_regex],
                                   min_length=1,
                                   max_length=2,
                                   label='CPU监控周期（单位小时，默认1小时）',
                                   required=True,
                                   widget=forms.NumberInput(attrs={"class": "form-control"}))
    # 内存监控周期
    mem_interval = forms.CharField(validators=[interval_regex],
                                   min_length=1,
                                   max_length=2,
                                   label='内存监控周期（单位小时，默认1小时）',
                                   required=True,
                                   widget=forms.NumberInput(attrs={"class": "form-control"}))
    # 速率监控周期
    speed_interval = forms.CharField(validators=[interval_regex],
                                     min_length=1,
                                     max_length=2,
                                     label='接口速率监控周期（单位小时，默认1小时）',
                                     required=True,
                                     widget=forms.NumberInput(attrs={"class": "form-control"}))
    # 利用率监控周期
    utilization_interval = forms.CharField(validators=[interval_regex],
                                           min_length=1,
                                           max_length=2,
                                           label='接口利用率监控周期（单位小时，默认1小时）',
                                           required=True,
                                           widget=forms.NumberInput(attrs={"class": "form-control"}))


# 系统设置, Netflow相关参数表单
class SysconfignetflowForm(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'
    lifetime_regex = RegexValidator(regex=r'^\d{1,5}$',
                                    message="老化时间只能支持最多5位整数")
    interval_regex = RegexValidator(regex=r'^\d{1,2}$',
                                    message="监控周期只能支持最多2位整数")
    # Netflow监控周期
    netflow_interval = forms.CharField(validators=[interval_regex],
                                       min_length=1,
                                       max_length=2,
                                       label='Netflow监控周期（单位小时，默认1小时）',
                                       required=True,
                                       widget=forms.NumberInput(attrs={"class": "form-control"}))
    # Netflow老化时间
    netflow_lifetime = forms.CharField(validators=[lifetime_regex],
                                       min_length=1,
                                       max_length=5,
                                       label='Netflow老化时间（单位小时，默认24小时）',
                                       required=True,
                                       widget=forms.NumberInput(attrs={"class": "form-control"}))


# 系统设置, 告警阈值,周期与SMTP相关表单
class Sysconfigthreshold(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'
    threshold_regex = RegexValidator(regex=r'^1?\d{1,2}$',
                                     message="阈值取值范围为1-100的整数")
    interval_regex = RegexValidator(regex=r'^\d{1,2}$',
                                    message="监控周期只能支持最多2位整数")
    # CPU告警阈值
    cpu_threshold = forms.CharField(validators=[threshold_regex],
                                    min_length=1,
                                    max_length=3,
                                    label='CPU告警阈值（单位%）设置为0表示取消',
                                    required=True,
                                    widget=forms.NumberInput(attrs={"class": "form-control"}))
    # CPU告警周期
    cpu_alarm_interval = forms.CharField(validators=[interval_regex],
                                         min_length=1,
                                         max_length=5,
                                         label='CPU告警周期（单位分钟）',
                                         required=True,
                                         widget=forms.NumberInput(attrs={"class": "form-control"}))
    # 内存告警阈值
    mem_threshold = forms.CharField(validators=[threshold_regex],
                                    min_length=1,
                                    max_length=3,
                                    label='内存告警阈值（单位%）设置为0表示取消',
                                    required=True,
                                    widget=forms.NumberInput(attrs={"class": "form-control"}))
    # 内存告警周期
    mem_alarm_interval = forms.CharField(validators=[interval_regex],
                                         min_length=1,
                                         max_length=5,
                                         label='内存告警周期（单位分钟）',
                                         required=True,
                                         widget=forms.NumberInput(attrs={"class": "form-control"}))
    # 接口利用率告警阈值
    utilization_threshold = forms.CharField(validators=[threshold_regex],
                                            min_length=1,
                                            max_length=3,
                                            label='接口利用率告警阈值（单位%）设置为0表示取消',
                                            required=True,
                                            widget=forms.NumberInput(attrs={"class": "form-control"}))
    # 接口利用率告警周期
    utilization_alarm_interval = forms.CharField(validators=[interval_regex],
                                                 min_length=1,
                                                 max_length=5,
                                                 label='接口利用率告警周期（单位分钟）',
                                                 required=True,
                                                 widget=forms.NumberInput(attrs={"class": "form-control"}))
    # SMTP邮件服务器
    mailserver = forms.CharField(min_length=1,
                                 max_length=50,
                                 label='邮件服务器',
                                 required=False,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    # SMTP认证用用户名
    mailusername = forms.CharField(min_length=1,
                                   max_length=50,
                                   label='用户名',
                                   required=False,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    # SMTP认证用密码
    mailpassword = forms.CharField(min_length=1,
                                   max_length=50,
                                   label='密码',
                                   required=False,
                                   widget=forms.TextInput(attrs={"class": "form-control"}))
    # 发件人
    mailfrom = forms.CharField(min_length=1,
                               max_length=50,
                               label='发件人FROM',
                               required=False,
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    # 收件人
    mailto = forms.CharField(min_length=1,
                             max_length=50,
                             label='收件人TO',
                             required=False,
                             widget=forms.TextInput(attrs={"class": "form-control"}))


# 自动化剧本, 找到IP所在接口表单
class FindifForm(forms.Form):
    # 如果希望出现必选左边的红色星标 ,必须配置下面的内容,并且在HTML中还要配置CSS
    required_css_class = 'required'
    ip = forms.GenericIPAddressField(required=True,
                                     label='IP地址',
                                     widget=forms.TextInput(attrs={"class": "form-control"}))