from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
# Register your models here.

# Override the default Django admin site header
class VoyaUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'mobile', 'login_type', 'is_active','date_joined')
    list_filter = ('login_type',)
    ordering = ['-date_joined']
    search_fields = ( 'email', 'first_name', 'mobile', 'login_type')

admin.site.register(User , VoyaUserAdmin)
admin.site.register(UserAddress)