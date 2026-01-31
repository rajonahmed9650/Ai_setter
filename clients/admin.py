from django.contrib import admin
from .models import Client,Tag,Tagged_lead
# Register your models here.
class ClientAmdin(admin.ModelAdmin):
    list_display = ("id","name","phone","email",)
admin.site.register(Client,ClientAmdin)
admin.site.register(Tag)
admin.site.register(Tagged_lead)