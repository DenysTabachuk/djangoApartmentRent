from django.urls import path
from . import views


urlpatterns = [
  path('<int:apartment_id>/', views.apartment_detail_view, name="apartment_detail"),
  # path("create/", views.apartment_create_view, name="apartment_create"),
  # path("edit/", views.apartment_edit_view, name="apartment_edit"),
  # path("delete/", views.apartment_delete_view, name="apartment_delete"),
]