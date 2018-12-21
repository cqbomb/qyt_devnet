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
from views import qyt_monitor_device, qyt_home, qyt_device_config

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.index),
    path('top/', top.top),
    path('top_json/', top.top_json),
    # 登录页面
    path('accounts/login/', qyt_login.qyt_login),
    # 注销页面
    path('accounts/logout/', qyt_login.qyt_logout),
    path('adddevices/', qyt_add_devices.add_devices),
    path('showdevices/', qyt_show_devices.show_devices),
    path('deletedevice/<str:devicename>/', qyt_del_device.del_device),
    path('editdevice/<str:devicename>/', qyt_edit_device.edit_device),
    path('monitordevice/cpu/', qyt_monitor_device.monitor_cpu),
    path('monitordevice/cpu/<str:devicename>/', qyt_monitor_device.monitor_cpu_dev),
    path('monitordevice/mem/', qyt_monitor_device.monitor_mem),
    path('monitordevice/mem/<str:devicename>/', qyt_monitor_device.monitor_mem_dev),
    path('monitordevice/if_speed/', qyt_monitor_device.monitor_if_speed),
    path('monitordevice/if_speed/<str:devicename>/', qyt_monitor_device.monitor_if_speed_dev),
    path('monitordevice/if_speed/<str:devicename>/<str:ifname>/<str:direction>', qyt_monitor_device.monitor_if_speed_dev_if_direc),
    path('monitordevice/if_utilization/', qyt_monitor_device.monitor_if_utilization),
    path('monitordevice/if_utilization/<str:devicename>/', qyt_monitor_device.monitor_if_utilization_dev),
    path('monitordevice/if_utilization/<str:devicename>/<str:ifname>/<str:direction>', qyt_monitor_device.monitor_if_utilization_dev_if_direc),
    path('home/reachable', qyt_home.health_reachable),
    path('home/cpu', qyt_home.health_cpu),
    path('home/mem', qyt_home.health_mem),
    path('deviceconfig/', qyt_device_config.device_config),
    path('deviceconfig/<str:devname>', qyt_device_config.device_config_dev),
    path('deviceconfig/delete/<str:devname>/<int:id>', qyt_device_config.device_del_config),
    path('deviceconfig/show/<str:devname>/<int:id>', qyt_device_config.device_show_config),
    path('deviceconfig/download/<str:devname>/<int:id>', qyt_device_config.device_download_config),
]
