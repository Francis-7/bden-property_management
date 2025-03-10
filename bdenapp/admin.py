from django.contrib import admin
from .models import Property, PropertyImage, Category

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'location', 'typeChoice']

@admin.register(PropertyImage)
class PropertyimageAdmin(admin.ModelAdmin):
    list_display = ['property']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']