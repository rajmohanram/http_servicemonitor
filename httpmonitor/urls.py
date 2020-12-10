from django.urls import path, include
from . import views


urlpatterns = [
    path('endpoints/', views.endpoints, name='httpmonitor.endpoints'),
    path('get-endpoint/', views.get_endpoint, name='httpmonitor.get-endpoint'),
    path('del-endpoint/', views.del_endpoint, name='httpmonitor.del-endpoint'),
    path('endpoints-status/', views.endpoints_status, name='httpmonitor.status'),
    path('get-services-up/', views.get_services_up, name='httpmonitor.get-services-up'),
    path('get-services-down/', views.get_services_down, name='httpmonitor.get-services-down'),
    path('check-state/', views.check_state, name='httpmonitor.check-state'),
]