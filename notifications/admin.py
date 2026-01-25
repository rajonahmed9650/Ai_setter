from django.contrib import admin
from .models import Notifications,Notifications_settings

# Register your models here.
class NotificationAdmin(admin.ModelAdmin):
    list_display =("id","message",)


admin.site.register(Notifications,NotificationAdmin)
admin.site.register(Notifications_settings)