from django.contrib import admin
from qytdb.models import Devicedb, Deviceconfig, Devicecpumem, Deviceinterfaces, Devicestatus

admin.site.register(Devicedb)
admin.site.register(Deviceconfig)
admin.site.register(Devicecpumem)
admin.site.register(Deviceinterfaces)
admin.site.register(Devicestatus)

