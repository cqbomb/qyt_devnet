"""qyt_devnet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from views import index, top, qyt_login, qyt_add_devices, qyt_show_devices, qyt_del_device, qyt_edit_device
from views import qyt_monitor_device, qyt_home, qyt_device_config, qyt_netflow, qyt_sysconfig, qyt_log, qyt_playbook
from views import qyt_show_devicetypes

urlpatterns = [
    path('admin/', admin.site.urls),  # 后台管理
    path('', index.index),  # 主页
    path('top/', top.top),  # 拓扑
    path('top_json/', top.top_json),  # 拓扑后台JSON数据
    path('accounts/login/', qyt_login.qyt_login),  # 登录页面
    path('accounts/logout/', qyt_login.qyt_logout),  # 注销页面
    path('adddevices/', qyt_add_devices.add_devices),  # 添加设备页面
    path('showdevices/', qyt_show_devices.show_devices),  # 查看设备状态页面
    path('showdevicetypes/', qyt_show_devicetypes.show_devicetypes),  # 查看设备类型页面
    path('deletedevice/<str:devicename>/', qyt_del_device.del_device),  # 删除设备页面
    path('editdevice/<str:devicename>/', qyt_edit_device.edit_device),  # 编辑设备页面
    path('monitordevice/cpu/', qyt_monitor_device.monitor_cpu),  # 监控CPU利用率默认页面
    path('monitordevice/cpu/<str:devicename>/', qyt_monitor_device.monitor_cpu_dev),  # 监控特定设备CPU利用率页面
    path('monitordevice/mem/', qyt_monitor_device.monitor_mem),  # 监控内存利用率默认页面
    path('monitordevice/mem/<str:devicename>/', qyt_monitor_device.monitor_mem_dev),  # 监控特定设备内存利用率页面
    path('monitordevice/if_speed/', qyt_monitor_device.monitor_if_speed),  # 监控接口速率默认页面
    path('monitordevice/if_speed/<str:devicename>/', qyt_monitor_device.monitor_if_speed_dev),  # 监控特定设备接口速率页面
    # 获取特定设备,特定接口,特定方向速率的JSON数据的URL链接
    path('monitordevice/if_speed/<str:devicename>/<str:ifname>/<str:direction>', qyt_monitor_device.monitor_if_speed_dev_if_direc),
    path('monitordevice/if_utilization/', qyt_monitor_device.monitor_if_utilization),  # 监控接口利用率默认页面
    path('monitordevice/if_utilization/<str:devicename>/', qyt_monitor_device.monitor_if_utilization_dev),  # 监控特定设备接口利用率页面
    # 获取特定设备,特定接口,特定方向利用率的JSON数据的URL链接
    path('monitordevice/if_utilization/<str:devicename>/<str:ifname>/<str:direction>', qyt_monitor_device.monitor_if_utilization_dev_if_direc),
    path('home/reachable', qyt_home.health_reachable),  # 主页获取设备健康摘要JSON数据的URL链接
    path('home/cpu', qyt_home.health_cpu),  # 主页获取CPU利用率摘要JSON数据的URL链接
    path('home/mem', qyt_home.health_mem),  # 主页获取内存利用率摘要JSON数据的URL链接
    path('deviceconfig/', qyt_device_config.device_config),  # 设备配置备份默认页面
    path('deviceconfig/<str:devname>', qyt_device_config.device_config_dev),  # 特定设备配置备份页面
    path('deviceconfig/delete/<str:devname>/<int:id>', qyt_device_config.device_del_config),  # 删除特定设备,特定配置备份URL链接
    path('deviceconfig/show/<str:devname>/<int:id>', qyt_device_config.device_show_config),  # 查看特定设备,特定配置备份页面
    path('deviceconfig/download/<str:devname>/<int:id>', qyt_device_config.device_download_config),  # 下载特定设备,特定配置备份URL链接
    path('deviceconfig/compare/<str:devname>/<int:id1>/<int:id2>', qyt_device_config.device_config_compare),  # 比较设备配置备份页面
    path('netflow/', qyt_netflow.netflow_show),  # 查看Netflow协议分析页面
    path('netflow/protocol', qyt_netflow.netflow_protocol),  # 获取Netflow 协议分布 Top 5 后台JSON数据URL链接
    path('netflow/top_ip', qyt_netflow.netflow_top_ip),  # 获取Netflow 最大流量IP Top 5 后台JSON数据URL链接
    path('sysconfig/lifetime', qyt_sysconfig.sysconfig_lifetime),  # 系统设置,老化时间页面
    path('sysconfig/monitor_interval', qyt_sysconfig.sysconfig_monitor_interval),  # 系统设置,监控周期页面
    path('sysconfig/threshold_mail', qyt_sysconfig.sysconfig_threshold_mail),  # 系统设置,告警阈值与邮件信息页面
    path('sysconfig/netflow', qyt_sysconfig.sysconfig_netflow),  # 系统设置,netflow相关参数页面
    path('sysconfig/reset_lifetime', qyt_sysconfig.sysconfig_reset_lifetime),  # 系统设置, 重置老化时间URL链接
    path('sysconfig/reset_monitor_interval', qyt_sysconfig.sysconfig_reset_monitor_interval),  # 系统设置,重置监控周期URL链接
    path('sysconfig/reset_threshold_mail', qyt_sysconfig.sysconfig_reset_threshold_mail),  # 系统设置, 重置告警阈值与邮件信息URL链接
    path('sysconfig/reset_netflow', qyt_sysconfig.sysconfig_reset_netflow),  # 重置Netflow相关参数URL链接
    path('sysconfig/reset_netflow_db', qyt_sysconfig.sysconfig_reset_netflow_db),  # 重置Netflow数据库URL链接
    path('log/elk', qyt_log.log_elk),  # 集成ELK页面
    path('playbook/find_if', qyt_playbook.find_if),  # 自动化剧本, 找到IP所在接口页面
]
