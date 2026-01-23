from django.contrib import admin
from .models import Conversation,Message
# Register your models here.

class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id","lead_id","source_id","current_state","last_message")

admin.site.register(Conversation,ConversationAdmin)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id","sender_type","message")

admin.site.register(Message,MessageAdmin)