from django.contrib import admin
from .models import Notifications,Notifications_settings

# Register your models here.
admin.site.register(Notifications)
admin.site.register(Notifications_settings)