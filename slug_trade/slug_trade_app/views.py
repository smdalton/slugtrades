from django.shortcuts import render
from django.contrib.auth.models import User
from .models import UserProfile
from . import models
# Create your views here.
debug = False


def index(request):
    test = "This was passed from the backend!"
    if debug:
        print("in index view")
    return render(request, 'slug_trade_app/index.html',{'test':test})

def products(request):
    return render(request, 'slug_trade_app/products.html')

# debug route
def show_users(request):
    users = User.objects.all()
    if debug:
        for item in users:
            print(item.userprofile)
    return render(request, 'slug_trade_app/users.html', {'users': users})

def profile(request):

    if request.user.is_authenticated():
        if debug:
            print(request.user)
        return render(request, 'slug_trade_app/profile.html', {'user': request.user})
    else:
        return render(request, 'slug_trade_app/not_authenticated.html')