from django.shortcuts import render
from django.contrib.auth.models import User
from . import models
from django.http import HttpResponseRedirect
import json
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

def edit_profile(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        data = request.POST

        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.userprofile.bio = data['bio']
        user.userprofile.on_off_campus = data['on_off_campus']
        user.userprofile.profile_picture = request.FILES['profile_picture']
        user.save()

        return HttpResponseRedirect('/slug_trade_app/profile/')
    else:
        if request.user.is_authenticated():
            return render(request, 'slug_trade_app/edit_profile.html', {'user': request.user})
        else:
            return render(request, 'slug_trade_app/not_authenticated.html')
