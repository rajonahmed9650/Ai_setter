from django.contrib import admin
from .models import Source
# Register your models here.
class SourceAdmin(admin.ModelAdmin):
    list_display = ("id","platform")

admin.site.register(Source,SourceAdmin)