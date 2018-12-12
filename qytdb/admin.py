from django.contrib import admin
from qytdb.models import Devicedb
from qytdb.models import Deviceconfig
from qytdb.models import Devicecpumem
from qytdb.models import Deviceinterfaces
from qytdb.models import Devicestatus
from qytdb.models import Device_reachable

admin.site.register(Devicedb)
admin.site.register(Deviceconfig)
admin.site.register(Devicecpumem)
admin.site.register(Deviceinterfaces)
admin.site.register(Devicestatus)
admin.site.register(Device_reachable)

