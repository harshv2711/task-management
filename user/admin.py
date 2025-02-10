from django.contrib import admin
from .models import CustomUser

# Django admin dashboard configuration 
admin.site.site_header = "Pivot Task Management"
admin.site.site_title = "Admin Dashboard"
admin.site.index_title = "Welcome to Admin Dashboard"

# Register your models here.
admin.site.register(CustomUser)