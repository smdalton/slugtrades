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

    # for each user we want to get the
    if debug:
        for item in users:
            print(item.userprofile)
    return render(request, 'slug_trade_app/users.html', {'users': users})
#
# def show_items(request):
#     # get items and item images by user
#     items = models.Item.objects.all()
#     users = User.objects.all()
#     images = models.ItemImage.all()
#
#     final_dict = {}
#
#     # for user in User.objects.all():
#     #     final_dict[user] = {}
#     #     for item in models.Item.objects.filter(user=user):
#     #         final_dict[user][item] = []
#     #         for image in models.ItemImage.objects.filter(item=item):
#     #             final_dict[user][item].append(image.image1.url)
#
#     return render(request, 'slug_trade_app/items.html',
#                   {
#                     'items': items,
#                     'users': users,
#                     'images': images
#                   })
#

def profile(request):
    if request.user.is_authenticated():
        if debug:
            print(request.user)
        return render(request, 'slug_trade_app/profile.html', {'user': request.user})
    else:
        return render(request, 'slug_trade_app/not_authenticated.html')