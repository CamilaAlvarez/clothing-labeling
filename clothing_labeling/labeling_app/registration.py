from django.shortcuts import render, redirect
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate, login
from .models import UserSpecifics


def register(request):
    return render(request, 'registration/register.html')

def verify(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            repeatPassword = request.POST['repeatPassword']
            if password!=repeatPassword:
                return render(request, 'registration/register.html', {'error':"Your passwords do not match!"})
            details = request.POST['info']
            other_details = "Amazon Mechanical Turk"
            mechanical_turk_user = True
            if details == 'other':
                other_details = request.POST['otherDetails']
                mechanical_turk_user = False

            if User.objects.filter(username=username):
                return render(request,'registration/register.html', {'error': 'Username already in use :('})

            new_user = User.objects.create_user(username=username, email=email, password=password)
            user_specifics = UserSpecifics(usr=new_user, usr_origin=other_details,
                                           usr_is_mechanical_turk=mechanical_turk_user)
            user_specifics.save()

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)

            return redirect('index')
        except KeyError:
            return render(request,'registration/register.html', {'error': 'Invalid data'})
    return redirect('register')