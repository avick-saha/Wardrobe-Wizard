from django.shortcuts import render, redirect 
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Upper

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        uppers = Upper.objects.filter(user=request.user)
        return render(request, 'home.html', {'uppers': uppers})
    else:
        message = "You have to be logged in to see your uploaded photos."
        return render(request, 'home.html', {'message': message})

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password
            =password)
            user.save()
            return redirect('user_login')
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')

def upload_upper(request):
    if not request.user.is_authenticated:
        message = "You have to be logged in to upload photos."
        return render(request, 'upload_upper.html', {'message': message})
    
    if request.method == 'POST' and request.FILES.get('upper'):
        upper = request.FILES['upper']
        Upper.objects.create(user=request.user, upper=upper)
        return redirect('home')
    
    return render(request, 'upload_upper.html')