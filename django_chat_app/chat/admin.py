from django.contrib import admin
from .models import Message

""" class MessageAdmin(admin.ModelAdmin):
    fields = ('test', 'created_at', 'author', 'receiver')
    list_display = ('test', 'created_at', 'author', 'receiver')
 """


# Register your models here.
admin.site.register(Message)