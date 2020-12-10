from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# home page
# /
@login_required()
def home(request):
    """View for home page of the project."""
    return render(request, 'svcmonitor/index.html')


# login page
# /login
def login(request):
    """View for login page of the project."""
    user_exist = User.objects.filter(username='admin')
    if not user_exist:
        admin_user = User.objects.create_user('admin', 'admin@example.com', 'admin', first_name = "Admin",
                                              last_name = "User", is_superuser = True)
        admin_user.save()
        app_user = User.objects.create_user('user', 'user@example.com', 'user', first_name="App",
                                              last_name="User", is_superuser=False)
        app_user.save()
    return render(request, 'svcmonitor/login.html')