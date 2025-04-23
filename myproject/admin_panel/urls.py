from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_panel_view, name='admin_panel'),
    path('moderate-apartment/<int:apartment_id>/', views.moderate_apartment_view, name='moderate_apartment'),
    path('toggle-user/<int:user_id>/', views.toggle_user_status_view, name='toggle_user_status'),
] 