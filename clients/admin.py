from django.contrib import admin

# Register your models here.

from .models import Clients, Interests, Clients_Interests

admin.site.register(Clients)
admin.site.register(Interests)
admin.site.register(Clients_Interests)