from django.urls import path, include
from . import views


urlpatterns = [
    path('auth/', views.authenticate_user, name='auth'),
    path('chpasswd/', views.change_password, name='chpasswd'),
    path('logout/', views.logout_user, name='logout'),
    path('user-mgmt/', views.users, name='usermgmt'),
    path('user-upd/', views.upd_user, name='updUser'),
    path('user-del/', views.del_user, name='delUser'),
]