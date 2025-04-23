from django.contrib import admin
from django.urls import path, include

handler404 = 'core.views.custom_error_handler_view'
handler403 = 'core.views.custom_error_handler_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('apartments/', include('apartments.urls')),
    path('admin-panel/', include('admin_panel.urls')),
    path('', include('core.urls')),
]
