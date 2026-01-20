from django.contrib import admin
from .models import Client,Tag,Tagged_lead
# Register your models here.

admin.site.register(Client)
admin.site.register(Tag)
admin.site.register(Tagged_lead)