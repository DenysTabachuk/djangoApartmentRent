from django.urls import  path
from . import views

urlpatterns = [
  path("login/", views.login_view, name="login"),
  path("register/", views.register_view, name="register"),
  path("profile/", views.profile_view, name="profile"),
  path("admin-panel/", views.admin_panel_view, name="admin-panel"),
  path("status/<int:apartment_id>", views.moderate_apartment_view, name="moderate-apartment"),
  path("<int:user_id>/toggle-status", views.toggle_user_status_view, name="toggle-user-status"),
  path("logout/", views.logout_view, name="logout"),
]
