from django.contrib import admin
from .models import Lead,LeadScoringRule,Question
# Register your models here.

class LeadAdmin(admin.ModelAdmin):
    list_display =("id","client_id","score","status")

admin.site.register(Lead,LeadAdmin)
admin.site.register(LeadScoringRule)
admin.site.register(Question)