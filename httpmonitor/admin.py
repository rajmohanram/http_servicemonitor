from django.contrib import admin
from .models import Endpoint, EndpointStatus

# Register your models here.
admin.site.register(Endpoint)
admin.site.register(EndpointStatus)