from django.contrib import admin
from .models import User,Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ("id","email","username")

    ordering=("id",)

admin.site.register(User,UserAdmin)
admin.site.register(Profile)


# Register your models here.
