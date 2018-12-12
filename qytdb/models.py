from django.db import models
from django.contrib.postgres.fields import JSONField


class Devicedb(models.Model):
    name = models.CharField(max_length=999, blank=False)
    ip = models.GenericIPAddressField(default='1.1.1.1')
    description = models.CharField(max_length=99999, blank=True)
    type = models.CharField(max_length=100, blank=False)
    snmp_enable = models.BooleanField(default=False)
    snmp_ro_community = models.CharField(max_length=999, blank=False)
    snmp_rw_community = models.CharField(max_length=999, blank=False)
    ssh_username = models.CharField(max_length=999, blank=False)
    ssh_password = models.CharField(max_length=999, blank=False)
    enable_password = models.CharField(max_length=999, blank=True)
    date = models.DateField(auto_now_add=True)


class Deviceinterfaces(models.Model):
    name = models.CharField(max_length=999, blank=False)
    interfaces = JSONField()
    interfaces_bw = JSONField()
    interfaces_max_utilization = JSONField()
    interfaces_current_utilization = JSONField()


class Devicecpumem(models.Model):
    name = models.CharField(max_length=999, blank=False)
    cpu_max_utilization = models.IntegerField(default=0, blank=True)
    cpu_current_utilization = models.IntegerField(default=0, blank=True)
    mem_max_utilization = models.IntegerField(default=0, blank=True)
    mem_current_utilization = models.IntegerField(default=0, blank=True)


class Devicestatus(models.Model):
    name = models.CharField(max_length=999, blank=False)
    interfaces = JSONField()
    interfaces_rx = JSONField()
    interfaces_tx = JSONField()
    cpu = models.IntegerField(default=0, blank=True)
    mem = models.IntegerField(default=0, blank=True)
    date = models.DateField(auto_now_add=True)


class Deviceconfig(models.Model):
    name = models.CharField(max_length=999, blank=False)
    hash = models.CharField(max_length=9999, blank=False)
    config = models.CharField(max_length=999999, blank=False)
    date = models.DateField(auto_now_add=True)


