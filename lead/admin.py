from django.contrib import admin
from .models import Lead,LeadScroingRule,Question
# Register your models here.

admin.site.register(Lead)
admin.site.register(LeadScroingRule)
admin.site.register(Question)