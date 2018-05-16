from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from .models import UserProfile
from slug_trade_app.forms import UserProfileForm, UserModelForm, ProfilePictureForm, ClosetItem, ClosetItemPhotos, UserForm, SignupUserProfileForm
from . import models
from slug_trade_app.models import ItemImage, Item, Wishlist
from slug_trade_app.models import UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
debug = False


def index(request):
    items = Item.objects.all()[:4]
    images = [ItemImage.objects.get(item=item).get_image_list() for item in items]
    items_and_images = zip(items,images)

    if debug:
        print("in index view")
    return render(request, 'slug_trade_app/index.html',{'items_and_images':items_and_images})


def products(request):
    categories = [
        { 'name': 'All', 'value': 'All' },
        { 'name': 'Electronics', 'value': 'E' },
        { 'name': 'Household goods', 'value': 'H' },
        { 'name': 'Clothing', 'value': 'C' },
        { 'name': 'Other', 'value': 'O' }
    ]
    if request.method == 'POST':
        if request.POST['category'] == 'All':
            items_list = ItemImage.objects.all()
        else:
            items_list = ItemImage.objects.all().filter(item__category=request.POST['category'])

        paginator = Paginator(items_list, 6) # Show 6 items per page
        page = request.GET.get('page', 1)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        return render(request, 'slug_trade_app/products.html', {'items': items, 'categories': categories, 'last_category': request.POST['category']})

    else:
        if request.user.is_authenticated():
            items_list = ItemImage.objects.all()
            paginator = Paginator(items_list, 6) # Show 6 items per page
            page = request.GET.get('page', 1)

            try:
                items = paginator.page(page)
            except PageNotAnInteger:
                items = paginator.page(1)
            except EmptyPage:
                items = paginator.page(paginator.num_pages)

            return render(request, 'slug_trade_app/products.html', {'items': items, 'categories': categories, 'last_category': 'All'})

        else:
            return render(request, 'slug_trade_app/not_authenticated.html')

# debug route
def show_users(request):
    users = User.objects.all()

    # for each user we want to get the
    if debug:
        for item in users:
            print(item.userprofile)
    return render(request, 'slug_trade_app/users.html', {'users': users})


def public_profile_inspect(request, user_id):

    """

        :param request: http request obj
        :param user_id: database key for specific user to load details about
        REQUIREMENTS: user_id exists in the database and it corresponds correctly
        to a specific user (numbers outside
        :return: render template
    """

    # verify that the given user_id is in the database, and if no prompt a redirect
    if not User.objects.filter(id=user_id).exists():
        return HttpResponse('<h1>No user exists for your query <a href="/">Go home</a></h1>')

    if request.user.is_authenticated() and int(user_id) == int(request.user.id):
        return redirect('/profile')

    # get the user model object
    user_to_view = User.objects.get(id=user_id)

    # get all of the items for the given user
    items = Item.objects.filter(user__id=user_id)

    # get the list of each item's images from the models method get_image_list()
    images = [ItemImage.objects.get(item=item).get_image_list() for item in items]
    # print(images)

    # zip the two lists into one iterable together
    items_and_images = zip(items, images)
    print("Items and images: ", items_and_images)

    wishlist = Wishlist.objects.filter(user=User.objects.get(id=user_id))

    return render(request, 'slug_trade_app/profile.html', {
                      'user_to_view': user_to_view,
                      'public': True,
                      'item_data': items_and_images,
                      'wishlist': wishlist,
                      'show_add_button': False
                  })


def profile(request):
    """
        profile is the view that handles authenticated users who have logged in
        by default it displays relevant information about the user, if no user
        is logged in, it will redirect to a sign-up/broken page
    """
    if request.user.is_authenticated():
        if request.method == 'POST':
            # if the wishlist item already exists in the wishlist, do not add it again
            try:
                existing_item = Wishlist.objects.get(user=request.user, wishlist_item_description=request.POST['description'])
            except Wishlist.DoesNotExist:
                item = Wishlist(
                        user = request.user,
                        wishlist_item_description = request.POST['description']
                    )
                item.save()
                return redirect('/profile?item_added=True')

        wishlist = Wishlist.objects.filter(user=request.user)
        items= Item.objects.filter(user__id=request.user.id)
        images= [ItemImage.objects.get(item=item).get_image_list() for item in items]
        items_and_images = zip(items,images)
        return render(request, 'slug_trade_app/profile.html', {
                    'user_to_view': request.user,
                    'public': False,
                    'item_data': items_and_images,
                    'wishlist': wishlist,
                    'show_add_button': True,
                    'item_added': request.GET.get('item_added', False)
                })
    else:
        return render(request, 'slug_trade_app/not_authenticated.html')

@csrf_exempt
def delete_from_wishlist(request):
    Wishlist.objects.get(id=request.POST['id']).delete()
    return HttpResponse('Deleted!')


def edit_profile(request):
    if request.method == 'POST':
        user_instance = User.objects.get(id=request.user.id)
        user_profile_instance = user_instance.userprofile
        user_form = UserModelForm(request.POST, instance=user_instance)
        user_profile_form = UserProfileForm(request.POST, instance=user_profile_instance)
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
        if user_profile_form.is_valid():
            user_profile_form.save()
        if profile_picture_form.is_valid() and request.FILES['file']:
            user_profile_instance.profile_picture = request.FILES['file']
            user_profile_instance.save()
        return redirect('/profile')
    else:
        if request.user.is_authenticated():
            user = User.objects.get(id=request.user.id)
            user_form = UserModelForm(instance=user)
            user_profile = user.userprofile
            user_profile_form = UserProfileForm(instance=user_profile)
            profile_picture_form = ProfilePictureForm()
            return render(request, 'slug_trade_app/edit_profile.html', {
                'user_form': user_form,
                'user_profile_form': user_profile_form,
                'profile_picture_form': profile_picture_form,
                'user': request.user
                })
        else:
            return render(request, 'slug_trade_app/not_authenticated.html')


def add_closet_item(request):
    if request.method == 'POST':
        form = ClosetItem(request.POST)
        photos = ClosetItemPhotos(request.POST, request.FILES)

        if form.is_valid():
            print('form is valid')
            item = form.save(commit=False)
            item.user = request.user
            if item.price < 0:
                item.price = 0
            form.save()

            if photos.is_valid():
                print('photos. is valid!')

                pics = []
                files = request.FILES

                if files.get('image1', False): pics.append(files['image1'])
                if files.get('image2', False): pics.append(files['image2'])
                if files.get('image3', False): pics.append(files['image3'])
                if files.get('image4', False): pics.append(files['image4'])
                if files.get('image5', False): pics.append(files['image5'])

                if len(pics) == 1:
                    insert = ItemImage(
                        item=item,
                        image1=pics[0]
                    )
                elif len(pics) == 2:
                    insert = ItemImage(
                        item=item,
                        image1=pics[0],
                        image2=pics[1]
                    )
                elif len(pics) == 3:
                    insert = ItemImage(
                        item=item,
                        image1=pics[0],
                        image2=pics[1],
                        image3=pics[2]
                    )
                elif len(pics) == 4:
                    insert = ItemImage(
                        item=item,
                        image1=pics[0],
                        image2=pics[1],
                        image3=pics[2],
                        image4=pics[3]
                    )
                elif len(pics) == 5:
                    insert = ItemImage(
                        item=item,
                        image1=pics[0],
                        image2=pics[1],
                        image3=pics[2],
                        image4=pics[3],
                        image5=pics[4]
                    )

                insert.save()

        return redirect('/profile')

    else:
        if request.user.is_authenticated():
            form = ClosetItem()
            photos = ClosetItemPhotos()
            return render(request, 'slug_trade_app/add_closet_item.html', {'form': form, 'photos': photos})
        else:
            return render(request, 'slug_trade_app/not_authenticated.html')


def signup(request):

    if request.user.is_authenticated():
        return redirect('/products')


    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = SignupUserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # create user
            created_user = user_form.save()

            created_user.username = created_user.email
            created_user.set_password(user_form.cleaned_data.get('password1'))
            created_user.save()

            # create extended profile
            created_profile = profile_form.save(commit=False)

            profile = UserProfile(
                user = created_user,
                profile_picture = request.FILES['profile_picture'],
                bio = created_profile.bio,
                on_off_campus = created_profile.on_off_campus
            )
            profile.save()

            # authentication
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password1')

            authenticated = authenticate(
                username=email,
                password=password
            )
            # if user is authenticated log them in and redirect
            if authenticated:
                login(request, authenticated)
                return redirect('/products')
            else:
                print("not authenticated")
                return redirect('/home')
        else:
            print("NOT VALID")
            return render(request, 'slug_trade_app/signup.html', {'user_form': user_form, 'profile_form': profile_form})

    else:
        user_form = UserForm()
        profile_form = SignupUserProfileForm()

        return render(request, 'slug_trade_app/signup.html', {'user_form': user_form, 'profile_form': profile_form})
