__copyright__ = "Copyright 2020 Birkbeck, University of London"
__author__ = "Martin Paul Eve, Andy Byers & Mauro Sanchez"
__license__ = "AGPL v3"
__maintainer__ = "Birkbeck Centre for Technology and Publishing"

from django.contrib import admin
from plugins.portico import models


class DeliveredAdmin(admin.ModelAdmin):
    list_display = ('issue', 'sent_at')
    list_filter = ('issue',)


admin_list = [
    (models.Delivered, DeliveredAdmin),
]

[admin.site.register(*t) for t in admin_list]