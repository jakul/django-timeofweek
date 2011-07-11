from django.contrib import admin
from timeofweek.models import Store


class StoreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Store, StoreAdmin)


