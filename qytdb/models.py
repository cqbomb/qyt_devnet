from django.db import models
from django.contrib.postgres.fields import JSONField


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


class Deviceinterfaces(models.Model):
    name = models.CharField(max_length=999, unique=True, blank=False)
    interfaces_num = models.IntegerField(default=0, blank=True)
    interfaces = JSONField(blank=True)
    interfaces_bw = JSONField(blank=True)
    interfaces_max_utilization = JSONField(blank=True)
    interfaces_current_utilization = JSONField(blank=True)


class Devicecpumem(models.Model):
    name = models.CharField(max_length=999, unique=True, blank=False)
    cpu_max_utilization = models.IntegerField(default=0, blank=True)
    cpu_current_utilization = models.IntegerField(default=0, blank=True)
    mem_max_utilization = models.IntegerField(default=0, blank=True)
    mem_current_utilization = models.IntegerField(default=0, blank=True)


class Devicestatus(models.Model):
    name = models.CharField(max_length=999, unique=True, blank=False)
    interfaces = JSONField(blank=True)
    interfaces_rx = JSONField(blank=True)
    interfaces_tx = JSONField(blank=True)
    cpu = models.IntegerField(default=0, blank=True)
    mem = models.IntegerField(default=0, blank=True)
    date = models.DateField(auto_now_add=True)


class Device_reachable(models.Model):
    name = models.CharField(max_length=999, unique=True, blank=False)
    snmp_reachable = models.BooleanField(default=False)
    ssh_reachable = models.BooleanField(default=False)


class Deviceconfig(models.Model):
    name = models.CharField(max_length=999, unique=True, blank=False)
    hash = models.CharField(max_length=9999, blank=False)
    config = models.CharField(max_length=999999, blank=False)
    date = models.DateField(auto_now_add=True)


