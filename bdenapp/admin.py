from django.contrib import admin
from .models import Property, PropertyImage

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'location', 'typeChoice']

@admin.register(PropertyImage)
class PropertyimageAdmin(admin.ModelAdmin):
    list_display = ['property']