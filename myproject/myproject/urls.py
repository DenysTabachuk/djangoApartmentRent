from django.contrib import admin
from django.urls import include, path

handler404 = 'core.views.custom_error_handler_view'
handler403 = 'core.views.custom_error_handler_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apartments/', include('apartments.urls')),  
    path('', include('users.urls')),  
    path('', include('core.urls')), 
]
