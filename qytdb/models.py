from django.db import models
from django.contrib.postgres.fields import JSONField


# 记录客户添加设备的基本信息,不随着时间的增加而增加!
class Devicedb(models.Model):
    name = models.CharField(max_length=999, unique=True, blank=False)
    ip = models.GenericIPAddressField(default='1.1.1.1', unique=True, )
    description = models.TextField(blank=True)
    type = models.CharField(max_length=100, blank=False)
    snmp_enable = models.BooleanField(default=False)
    snmp_ro_community = models.CharField(max_length=999, blank=False)
    snmp_rw_community = models.CharField(max_length=999, blank=True)
    ssh_username = models.CharField(max_length=999, blank=False)
    ssh_password = models.CharField(max_length=999, blank=False)
    enable_password = models.CharField(max_length=999, blank=True)
    date = models.DateField(auto_now_add=True)


# 记录设备接口的基本信息,不随着时间的增加而增加!
class Deviceinterfaces(models.Model):
    name = models.CharField(max_length=999, unique=True, blank=False)
    # 接口数量
    interfaces_num = models.IntegerField(default=0, blank=True)
    # 接口名字的清单
    interfaces = models.CharField(max_length=99999, blank=True)
    # 接口物理带宽的清单
    interfaces_bw = models.CharField(max_length=99999, blank=True)


# 记录设备接口当前状态信息,根据表Devicestatus记录的原始信息进行加工,随着时间的增长会不断添加条目,更新周期1分钟
class Deviceinterfaces_utilization(models.Model):
    name = models.CharField(max_length=999, blank=False)
    # 接口物理带宽的清单
    interfaces_bw = models.CharField(max_length=99999, blank=True)
    # 接口历史曾经最大利用率的清单(入向)
    interfaces_max_utilization_rx = models.CharField(max_length=99999, blank=True)
    # 接口当前速率的清单(入向)
    interfaces_current_speed_rx = models.CharField(max_length=99999, blank=True)
    # 接口当前利用率的清单(入向)
    interfaces_current_utilization_rx = models.CharField(max_length=99999, blank=True)
    # 接口历史曾经最大利用率的清单(出向)
    interfaces_max_utilization_tx = models.CharField(max_length=99999, blank=True)
    # 接口当前速率的清单(出向)
    interfaces_current_speed_tx = models.CharField(max_length=99999, blank=True)
    # 接口当前利用率的清单(出向)
    interfaces_current_utilization_tx = models.CharField(max_length=99999, blank=True)
    # 记录条目的时间
    date = models.DateTimeField(auto_now_add=True)


# 设备CPU和内存利用率表,记录当前内存和CPU利用率,和历史曾经内存和CPU的最大利用率,不随着时间的增加而增加!
class Devicecpumem(models.Model):
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
    name = models.CharField(max_length=999, unique=True, blank=False)
    # SNMP可达性
    snmp_reachable = models.BooleanField(default=False)
    # SSH可达性
    ssh_reachable = models.BooleanField(default=False)


# 保存设备配置,配置HASH和时间
class Deviceconfig(models.Model):
    name = models.CharField(max_length=999, blank=False)
    # 配置HASH值,便于快速比较
    hash = models.CharField(max_length=9999, blank=False)
    # 保存的设备配置
    config = models.CharField(max_length=999999, blank=False)
    # 备份配置的时间
    date = models.DateTimeField(auto_now_add=True)


# Netflow DB
class Netflow(models.Model):
    src_ip = models.CharField(max_length=999, blank=False)

    dst_ip = models.CharField(max_length=999, blank=False)

    protocol = models.IntegerField(blank=True)

    src_port = models.IntegerField(blank=True)

    dst_port = models.IntegerField(blank=True)

    in_if_id = models.IntegerField(blank=True)

    in_bytes = models.IntegerField(blank=True)

    date = models.DateTimeField(auto_now_add=True)


class LifetimeNetflow(models.Model):
    lifetime = models.IntegerField(blank=False)


class LifetimeDevicestatus(models.Model):
    lifetime = models.IntegerField(blank=False)


class Devicemonitorintervalcpu(models.Model):
    cpu_interval = models.IntegerField(blank=False)


class Devicemonitorintervalmem(models.Model):
    mem_interval = models.IntegerField(blank=False)


class Devicemonitorintervalspeed(models.Model):
    speed_interval = models.IntegerField(blank=False)


class Devicemonitorintervalutilization(models.Model):
    utilization_interval = models.IntegerField(blank=False)


class Netflowinterval(models.Model):
    netflow_interval = models.IntegerField(blank=False)


class Thresholdcpu(models.Model):
    cpu_threshold = models.IntegerField(blank=False)
    alarm_interval = models.IntegerField(blank=False)
    last_alarm_time = models.DateTimeField(auto_now_add=True)


class Thresholdmem(models.Model):
    mem_threshold = models.IntegerField(blank=False)


class Thresholdutilization(models.Model):
    utilization_threshold = models.IntegerField(blank=False)


class Smtplogindb(models.Model):
    mailserver = models.CharField(max_length=999, blank=False)
    mailusername = models.CharField(max_length=999, blank=False)
    mailpassword = models.CharField(max_length=999, blank=False)
    mailfrom = models.CharField(max_length=999, blank=False)
    mailto = models.CharField(max_length=999, blank=False)

