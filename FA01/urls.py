from django.urls import path
from . import views
from .views import RegistroDispositivosAPIView, SucursalDispositivosAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/<int:pk>/', views.asset_detail, name='asset_detail'),
    path('assets/create/', views.asset_create, name='asset_create'),
    path('assets/<int:pk>/update/', views.asset_update, name='asset_update'),
    path('locations/', views.location_list, name='location_list'),
    path('locations/create/', views.location_create, name='location_create'),
    path('locations/<int:pk>/update/', views.location_update, name='location_update'),
    path('locations/export/', views.export_locations_excel, name='export_locations_excel'),
    path('locations/import/', views.import_locations_excel, name='import_locations_excel'),
    path('movements/create/', views.movement_create, name='movement_create'),
    path('profile/', views.user_profile, name='user_profile'),
    path('assets/export/', views.export_assets_excel, name='export_assets_excel'),
    path('assets/template/', views.export_assets_template, name='export_assets_template'),
    path('assets/import/', views.import_assets_excel, name='import_assets_excel'),
    path('assets/image/<int:image_id>/delete/', views.delete_asset_image, name='delete_asset_image'),
    path('logout/', views.custom_logout, name='logout'),
    path('network-scan/', views.network_scan, name='network_scan'),
    path('network-devices/', views.network_devices, name='network_devices'),
    path('add-network-device/', views.add_network_device, name='add_network_device'),
    path('api/registro/', RegistroDispositivosAPIView.as_view(), name='api_registro'),
    path('api/sucursal/<str:codigo>/', SucursalDispositivosAPIView.as_view(), name='api_sucursal_dispositivos'),
    path('assets/letter_responsibility/<int:image_id>/delete/', views.delete_asset_letter_responsibility, name='delete_asset_letter_responsibility'),
]