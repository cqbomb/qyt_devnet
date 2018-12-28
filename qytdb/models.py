from django.db import models
from django.contrib.postgres.fields import JSONField


# 记录客户添加设备的基本信息,不随着时间的增加而增加!
class Devicedb(models.Model):
    # 设备名称
    name = models.CharField(max_length=999, unique=True, blank=False)
    # 设备IP地址
    ip = models.GenericIPAddressField(default='1.1.1.1', unique=True)
    # 设备描述信息
    description = models.TextField(blank=True)
    # 设备类型
    type = models.CharField(max_length=100, blank=False)
    # SNMP是否激活
    snmp_enable = models.BooleanField(default=False)
    # SNMP只读Community
    snmp_ro_community = models.CharField(max_length=999, blank=False)
    # SNMP读写Community
    snmp_rw_community = models.CharField(max_length=999, blank=True)
    # SSH用户名
    ssh_username = models.CharField(max_length=999, blank=False)
    # SSH密码
    ssh_password = models.CharField(max_length=999, blank=False)
    # 特权密码(ASA必须设置)
    enable_password = models.CharField(max_length=999, blank=True)
    # 添加设备时间
    date = models.DateField(auto_now_add=True)


# 记录设备接口的基本信息,不随着时间的增加而增加!
class Deviceinterfaces(models.Model):
    # 设备名称
    name = models.CharField(max_length=999, unique=True, blank=False)
    # 接口数量
    interfaces_num = models.IntegerField(default=0, blank=True)
    # 接口名字的清单(会以JSON数据的方式进行保存)
    interfaces = models.CharField(max_length=99999, blank=True)
    # 接口物理带宽的清单(会以JSON数据的方式进行保存)
    interfaces_bw = models.CharField(max_length=99999, blank=True)


# 记录设备接口当前状态信息,根据表Devicestatus记录的原始信息进行加工,随着时间的增长会不断添加条目,更新周期1分钟
class Deviceinterfaces_utilization(models.Model):
    # 设备名称
    name = models.CharField(max_length=999, blank=False)
    # 接口物理带宽的清单(会以JSON数据的方式进行保存)
    interfaces_bw = models.CharField(max_length=99999, blank=True)
    # 接口历史曾经最大利用率的清单(入向)(会以JSON数据的方式进行保存)

    interfaces_max_utilization_rx = models.CharField(max_length=99999, blank=True)
    # 接口当前速率的清单(入向)(会以JSON数据的方式进行保存)
    interfaces_current_speed_rx = models.CharField(max_length=99999, blank=True)
    # 接口当前利用率的清单(入向)(会以JSON数据的方式进行保存)
    interfaces_current_utilization_rx = models.CharField(max_length=99999, blank=True)
    # 接口历史曾经最大利用率的清单(出向)(会以JSON数据的方式进行保存)

    interfaces_max_utilization_tx = models.CharField(max_length=99999, blank=True)
    # 接口当前速率的清单(出向)(会以JSON数据的方式进行保存)
    interfaces_current_speed_tx = models.CharField(max_length=99999, blank=True)
    # 接口当前利用率的清单(出向)(会以JSON数据的方式进行保存)
    interfaces_current_utilization_tx = models.CharField(max_length=99999, blank=True)
    # 记录条目的时间
    date = models.DateTimeField(auto_now_add=True)


# 设备类型,名称,SNMPOID
class DevicetypeSNMP(models.Model):
    # 设备类型
    type = models.CharField(max_length=999, blank=False)
    # 设备类型名称
    type_name = models.CharField(max_length=999, blank=False)
    # SNMP OID CPU
    cpu_oid = models.CharField(max_length=999, blank=False)
    # SNMP OID MEM Free
    mem_free_oid = models.CharField(max_length=999, blank=False)
    # SNMP OID MEM Used
    mem_used_oid = models.CharField(max_length=999, blank=False)
    # SNMP OID interfaces name list
    interfaces_name_oid = models.CharField(max_length=999, blank=False)
    # SNMP OID interfaces bw list
    interfaces_bw_oid = models.CharField(max_length=999, blank=False)
    # SNMP OID interfaces in bytes list
    interfaces_in_bytes_oid = models.CharField(max_length=999, blank=False)
    # SNMP OID interfaces out bytes list
    interfaces_out_bytes_oid = models.CharField(max_length=999, blank=False)


# 设备CPU和内存利用率表,记录当前内存和CPU利用率,和历史曾经内存和CPU的最大利用率,不随着时间的增加而增加!
class Devicecpumem(models.Model):
    # 设备名称
    name = models.CharField(max_length=999, unique=True, blank=False)
    # 历史曾经最大CPU利用率
    cpu_max_utilization = models.IntegerField(default=0, blank=True)
    # 当前CPU利用率
    cpu_current_utilization = models.IntegerField(default=0, blank=True)
    # 历史曾经最大内存利用率
    mem_max_utilization = models.IntegerField(default=0, blank=True)
    # 当前内存利用率
    mem_current_utilization = models.IntegerField(default=0, blank=True)


# 记录设备原始信息的流水账,包含接口名称的列表,接口收发字节数的列表,cpu和内存利用率
# 随着时间的增长会不断添加条目,更新周期1分钟
class Devicestatus(models.Model):
    # 设备名称
    name = models.CharField(max_length=999, blank=False)
    # 接口名称的列表
    interfaces = models.CharField(max_length=99999, blank=True)
    # 接口入向字节数列表
    interfaces_rx = models.CharField(max_length=99999, blank=True)
    # 接口出向字节数列表
    interfaces_tx = models.CharField(max_length=99999, blank=True)
    # CPU利用率
    cpu = models.IntegerField(default=0, blank=True)
    # 内存利用率
    mem = models.IntegerField(default=0, blank=True)
    # 记录条目的时间
    date = models.DateTimeField(auto_now_add=True)


# 记录设备可达性信息,不随着时间的增加而增加!
class Device_reachable(models.Model):
    # 设备名称
    name = models.CharField(max_length=999, unique=True, blank=False)
    # SNMP可达性
    snmp_reachable = models.BooleanField(default=False)
    # SSH可达性
    ssh_reachable = models.BooleanField(default=False)


# 保存设备配置,配置HASH和时间
class Deviceconfig(models.Model):
    # 设备名称
    name = models.CharField(max_length=999, blank=False)
    # 配置HASH值,便于快速比较
    hash = models.CharField(max_length=9999, blank=False)
    # 保存的设备配置
    config = models.CharField(max_length=999999, blank=False)
    # 备份配置的时间
    date = models.DateTimeField(auto_now_add=True)


# Netflow数据库
class Netflow(models.Model):
    # 源IP地址
    src_ip = models.CharField(max_length=999, blank=False)
    # 目的IP地址
    dst_ip = models.CharField(max_length=999, blank=False)
    # 协议
    protocol = models.IntegerField(blank=True)
    # 源端口
    src_port = models.IntegerField(blank=True)
    # 目的端口
    dst_port = models.IntegerField(blank=True)
    # 入向接口ID
    in_if_id = models.IntegerField(blank=True)
    # 入向字节数
    in_bytes = models.IntegerField(blank=True)
    # 数据记录时间
    date = models.DateTimeField(auto_now_add=True)


class LifetimeNetflow(models.Model):
    # Netflow数据老化时间
    lifetime = models.IntegerField(blank=False)


class LifetimeDevicestatus(models.Model):
    # 设备状态信息老化时间
    lifetime = models.IntegerField(blank=False)


class Devicemonitorintervalcpu(models.Model):
    # CPU 监控周期
    cpu_interval = models.IntegerField(blank=False)


class Devicemonitorintervalmem(models.Model):
    # 内存 监控周期
    mem_interval = models.IntegerField(blank=False)


class Devicemonitorintervalspeed(models.Model):
    # 接口速率监控周期
    speed_interval = models.IntegerField(blank=False)


class Devicemonitorintervalutilization(models.Model):
    # 接口利用率监控周期
    utilization_interval = models.IntegerField(blank=False)


class Netflowinterval(models.Model):
    # Netflow 监控周期
    netflow_interval = models.IntegerField(blank=False)


class Thresholdcpu(models.Model):
    # CPU 告警阈值
    cpu_threshold = models.IntegerField(blank=False)
    # CPU 告警周期
    alarm_interval = models.IntegerField(blank=False)
    # 上一次CPU告警时间
    last_alarm_time = models.DateTimeField(auto_now_add=True)


class Thresholdmem(models.Model):
    # 内存 告警阈值
    mem_threshold = models.IntegerField(blank=False)
    # 内存 告警周期
    alarm_interval = models.IntegerField(blank=False)
    # 上一次内存告警时间
    last_alarm_time = models.DateTimeField(auto_now_add=True)


class Thresholdutilization(models.Model):
    # 接口利用率 告警阈值
    utilization_threshold = models.IntegerField(blank=False)
    # 接口利用率 告警周期
    alarm_interval = models.IntegerField(blank=False)
    # 上一次接口利用率告警时间
    last_alarm_time = models.DateTimeField(auto_now_add=True)


class Smtplogindb(models.Model):
    # SMTP邮件服务器
    mailserver = models.CharField(max_length=999, blank=False)
    # SMTP邮件服务器认证用户名
    mailusername = models.CharField(max_length=999, blank=False)
    # SMTP邮件服务器认证密码
    mailpassword = models.CharField(max_length=999, blank=False)
    # 发件人
    mailfrom = models.CharField(max_length=999, blank=False)
    # 收件人
    mailto = models.CharField(max_length=999, blank=False)

