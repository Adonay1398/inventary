from django.contrib import admin
from .models import (
    Asset, Location, Movement, UserProfile, Sucursal, 
    DispositivoSucursal, AssetImage, Responsibility
)

# Register your models here.
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'serial_number', 'category', 'status', 'location', 'assigned_to']
    list_filter = ['category', 'status', 'location', 'purchase_date']
    search_fields = ['name', 'serial_number', 'brand', 'model']
    date_hierarchy = 'created_at'

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location_type', 'created_at']
    list_filter = ['location_type']
    search_fields = ['name']

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ['asset', 'movement_date', 'from_location', 'to_location']
    list_filter = ['movement_date']
    date_hierarchy = 'movement_date'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'position']
    search_fields = ['user__username', 'department', 'position']

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'responsable']
    search_fields = ['nombre', 'codigo']

@admin.register(DispositivoSucursal)
class DispositivoSucursalAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'ip', 'mac', 'sucursal', 'fecha_envio']
    list_filter = ['sucursal', 'fecha_envio']
    search_fields = ['hostname', 'ip', 'mac']

@admin.register(AssetImage)
class AssetImageAdmin(admin.ModelAdmin):
    list_display = ['asset', 'uploaded_at']
    list_filter = ['uploaded_at']
    date_hierarchy = 'uploaded_at'

@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = ['asset', 'uploaded_at']
    list_filter = ['uploaded_at']
    date_hierarchy = 'uploaded_at'
