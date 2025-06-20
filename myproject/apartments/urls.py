from django.urls import path
from . import views


urlpatterns = [
  path('', views.apartments_view, name='apartments'),
  path('create/', views.apartment_create_view, name='apartment_create'),
  path('<int:apartment_id>/edit/', views.apartment_edit_view, name='apartment_edit'),
  path('<int:apartment_id>/delete/', views.apartment_delete_view, name='apartment_delete'),
  path('<int:apartment_id>/', views.apartment_detail_view, name='apartment_detail'),
]
