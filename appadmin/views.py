from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# https://docs.djangoproject.com/en/3.1/topics/auth/default/
# /app/auth
def authenticate_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        context = {'error': 'User authentication failed.'}
        return render(request, 'svcmonitor/login.html', context=context)


# /app/chpasswd
def change_password(request):
    password = request.POST.get('password')
    user = User.objects.get(username=request.user.username)
    try:
        user.set_password(password)
        user.save()
        return redirect('logout')
    except:
        return HttpResponse('password not changed')


# /app/logout
def logout_user(request):
    logout(request)
    return redirect('home')


# /app/user-mgmt
@login_required()
def users(request):
    """View for managing users."""
    if request.method == 'GET':
        users = User.objects.all()
        context = {"users": users}
        return render(request, 'appadmin/users.html', context=context)
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('dname')
        User.objects.create_user(username.lower(), password="user@123", first_name=firstname)
        return redirect('usermgmt')


# /app/upd-user
@login_required()
def upd_user(request):
    """View for update a user."""
    id = request.POST.get('id')
    enabled = request.POST.get('enabled')
    password = request.POST.get('password')
    user = User.objects.get(id=id)
    if password is not None:
        try:
            user.set_password(password)
        except:
            return HttpResponse('password not changed')
    if enabled is not None:
        user.is_active = True
    else:
        user.is_active = False
    user.save()
    return redirect('usermgmt')


# /app/del-user?id=10
@login_required()
def del_user(request):
    """View for deleting a user."""
    id = request.GET.get('id')
    User.objects.filter(id=id).delete()
    return redirect('usermgmt')