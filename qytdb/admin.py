from django.contrib import admin
from qytdb.models import Devicedb
from qytdb.models import Deviceconfig
from qytdb.models import Devicecpumem
from qytdb.models import Deviceinterfaces
from qytdb.models import Devicestatus
from qytdb.models import Device_reachable
from qytdb.models import Deviceinterfaces_utilization
from qytdb.models import Devicemonitorintervalspeed
from qytdb.models import Devicemonitorintervalutilization
from qytdb.models import Devicemonitorintervalcpu
from qytdb.models import Devicemonitorintervalmem
from qytdb.models import Netflowinterval
from qytdb.models import Netflow
from qytdb.models import LifetimeDevicestatus
from qytdb.models import LifetimeNetflow
from qytdb.models import Thresholdcpu
from qytdb.models import Thresholdmem
from qytdb.models import Thresholdutilization
from qytdb.models import Smtplogindb

admin.site.register(Devicedb)
admin.site.register(Deviceconfig)
admin.site.register(Devicecpumem)
admin.site.register(Deviceinterfaces)
admin.site.register(Devicestatus)
admin.site.register(Device_reachable)
admin.site.register(Deviceinterfaces_utilization)
admin.site.register(Devicemonitorintervalspeed)
admin.site.register(Devicemonitorintervalutilization)
admin.site.register(Devicemonitorintervalcpu)
admin.site.register(Devicemonitorintervalmem)
admin.site.register(Netflowinterval)
admin.site.register(Netflow)
admin.site.register(LifetimeDevicestatus)
admin.site.register(LifetimeNetflow)
admin.site.register(Thresholdcpu)
admin.site.register(Thresholdmem)
admin.site.register(Thresholdutilization)
admin.site.register(Smtplogindb)


