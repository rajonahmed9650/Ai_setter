from django.contrib import admin
from .models import Lead,LeadScoringRule,Question
# Register your models here.

admin.site.register(Lead)
admin.site.register(LeadScoringRule)
admin.site.register(Question)