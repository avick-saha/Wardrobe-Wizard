from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')

def signupUser(request):
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
    return render(request, 'signup.html')