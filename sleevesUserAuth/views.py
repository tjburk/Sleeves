from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request,user)
                return redirect("/")
    else:
        form = LoginForm()
    return render(request, 'sleevesUserAuth/login.html', {'form':form})


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        else: 
            return render(request, 'sleevesUserAuth/signUp.html', {"form":form})
    else:
        form = UserCreationForm()
        return render(request, 'sleevesUserAuth/signUp.html', {"form":form})
    
    #BerfectPoor23