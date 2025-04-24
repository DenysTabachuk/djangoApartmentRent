from django.contrib import admin
from .models import Apartment

class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'owner', 'get_city', 'status')
    list_filter = ('status', 'owner', 'location')
    search_fields = ('title', 'description', 'location')
    
    # Метод для витягування міста з JSON-поля location.
    def get_city(self, obj):
        return obj.location.get('city', '')
    

admin.site.register(Apartment, ApartmentAdmin)
