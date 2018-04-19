from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from slug_trade_app.forms import UserForm, UserProfileForm
from . import models
# Create your views here.

def index(request):
    test = "This was passed from the backend!"
    print("in index view")
    return render(request, 'slug_trade_app/index.html',{'test':test})

def products(request):
    return render(request, 'slug_trade_app/products.html')

def profile(request):

    if request.user.is_authenticated():
        print(request.user)
        return render(request, 'slug_trade_app/profile.html', {'user': request.user})
    else:
        return render(request, 'slug_trade_app/not_authenticated.html')

def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()

            user = authenticate(username=user_form.cleaned_data['email'],
                                    password=user_form.cleaned_data['password1'],
                                    )
            login(request, user)
            return redirect('/home')
    else:
        user_form = UserForm()

        return render(request, 'slug_trade_app/signup.html', {'user_form': user_form})
