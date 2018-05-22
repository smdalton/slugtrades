from django.http import HttpResponse,  HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from .models import UserProfile
from slug_trade_app.forms import UserProfileForm, UserModelForm, ProfilePictureForm, ClosetItem, ClosetItemPhotos, UserForm, SignupUserProfileForm
from . import models
from slug_trade_app.models import ItemImage, Item, Wishlist
from slug_trade_app.models import UserProfile, ITEM_CATEGORIES, TRADE_OPTIONS
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
debug = False


def index(request):
    items = Item.objects.all()[:4]
    images = [ItemImage.objects.get(item=item).get_image_list() for item in items]
    items_and_images = zip(items,images)

    books = Item.objects.filter(category="BO")[:4]
    b_images = [ItemImage.objects.get(item=book).get_image_list() for book in books]
    books_and_images = zip(books,b_images)

    popular = Item.objects.all().order_by('-bid_counter')[:4]
    p_images = [ItemImage.objects.get(item=p).get_image_list() for p in popular]
    popular_and_images = zip(popular,p_images)

    recent = Item.objects.all().order_by('-time_stamp')[:4]
    r_images = [ItemImage.objects.get(item=r).get_image_list() for r in recent]
    recent_and_images = zip(recent,r_images)


    if debug:
        print("in index view")

    categories = [
        { 'name': 'All', 'value': 'All' }
    ]
    types = [
        { 'name': 'All', 'value': 'All' }
    ]

    for value, name in ITEM_CATEGORIES:
        categories.append({ 'name': name, 'value': value})

    for value, name in TRADE_OPTIONS:
        types.append({ 'name': name, 'value': value })

    print("At home")
    return render(request, 'slug_trade_app/index.html',{
        'items_and_images':items_and_images,
        'books_and_images': books_and_images,
        'popular_and_images': popular_and_images,
        'recent_and_images': recent_and_images,
        'categories': categories,
        'types': types
    })


def products(request):

    categories = []
    category_values = []
    selected_values = []

    types = []
    type_values = []
    selected_types = []

    for value, name in ITEM_CATEGORIES:
        categories.append({ 'name': name, 'value': value})
        category_values.append(value)

    for value, name in TRADE_OPTIONS:
        types.append({ 'name': name, 'value': value })
        type_values.append(value)

    if request.user.is_authenticated():
        items_list = ItemImage.objects.all()

        if request.GET.get('categories', False):
            selected_values = []
            for key, values in request.GET.lists():
                if key =='categories':
                    for value in values:
                        selected_values.append(value)

            for category in category_values:
                if category not in selected_values:
                    items_list = items_list.exclude(item__category=category)

        if request.GET.get('types', False):
            selected_types = []
            for key, values in request.GET.lists():
                if key =='types':
                    for value in values:
                        selected_types.append(value)

            for type in type_values:
                if type not in selected_types:
                    items_list = items_list.exclude(item__trade_options=type)

        item_count = items_list.count()
        paginator = Paginator(items_list, 12) # Alter the second parameter to change number of items per page
        page = request.GET.get('page', 1)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        return render(request, 'slug_trade_app/products.html', {'items': items, 'categories': categories, 'selected_values': selected_values, 'types': types, 'selected_types': selected_types, 'item_count': item_count})

    else:
        return render(request, 'slug_trade_app/not_authenticated.html')

# debug route
def show_users(request):
    users = User.objects.all()

    # for each user we want to get the
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
    items_list = Item.objects.filter(user__id=user_id)

    paginator = Paginator(items_list, 6)
    page = request.GET.get('page', 1)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    images= [ItemImage.objects.get(item=item).get_image_list() for item in items]
    items_and_images = zip(items,images)

    wishlist = Wishlist.objects.filter(user=User.objects.get(id=user_id))

    return render(request, 'slug_trade_app/profile.html', {
                      'user_to_view': user_to_view,
                      'public': True,
                      'item_data': items_and_images,
                      'wishlist': wishlist,
                      'show_add_button': False,
                      'items': items
                  })


def profile(request):
    """
        profile is the view that handles authenticated users who have logged in
        by default it displays relevant information about the user, if no user
        is logged in, it will redirect to a sign-up/broken page
    """
    if request.user.is_authenticated():
        if request.method == 'POST' and not request.POST['description'].isspace() and not request.POST['description'] == '':
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
        items_list= Item.objects.filter(user__id=request.user.id)

        paginator = Paginator(items_list, 6)
        page = request.GET.get('page', 1)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        images= [ItemImage.objects.get(item=item).get_image_list() for item in items]
        items_and_images = zip(items,images)

        return render(request, 'slug_trade_app/profile.html', {
                    'user_to_view': request.user,
                    'public': False,
                    'item_data': items_and_images,
                    'wishlist': wishlist,
                    'show_add_button': True,
                    'item_added': request.GET.get('item_added', False),
                    'items': items,
                    'my_profile': True
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

        pics = []
        files = request.FILES

        if files.get('image1', False): pics.append(files['image1'])
        if files.get('image2', False): pics.append(files['image2'])
        if files.get('image3', False): pics.append(files['image3'])
        if files.get('image4', False): pics.append(files['image4'])
        if files.get('image5', False): pics.append(files['image5'])

        image1 = pics.pop(0)

        if len(pics) >= 1:
            image2 = pics.pop(0);
        else:
            image2 = None
        if len(pics) >= 1:
            image3 = pics.pop(0);
        else:
            image3 = None
        if len(pics) >= 1:
            image4 = pics.pop(0);
        else:
            image4 = None
        if len(pics) >= 1:
            image5 = pics.pop(0);
        else:
            image5 = None

        photos_data = {
            'image1': image1,
            'image2': image2,
            'image3': image3,
            'image4': image4,
            'image5': image5
        }

        photos = ClosetItemPhotos(request.POST, photos_data)

        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            if item.price < 0:
                item.price = 0
            form.save()

            if photos.is_valid():
                insert = ItemImage(
                    item = item,
                    image1 = image1,
                    image2 = image2,
                    image3 = image3,
                    image4 = image4,
                    image5 = image5
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

def edit_closet_item(request):
    if request.method == 'POST':
        item_images_instance = ItemImage.objects.get(id=request.POST.get('id', None))
        item_instance = item_images_instance.item

        form = ClosetItem(request.POST, instance=item_instance)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            if item.price < 0:
                item.price = 0
            form.save()

            files = request.FILES
            temps = request.POST

            image1 = files.get('image1', '')
            image2 = files.get('image2', '')
            image3 = files.get('image3', '')
            image4 = files.get('image4', '')
            image5 = files.get('image5', '')

            temp1 = temps.get('temp-image1', '')
            temp2 = temps.get('temp-image2', '')
            temp3 = temps.get('temp-image3', '')
            temp4 = temps.get('temp-image4', '')
            temp5 = temps.get('temp-image5', '')

            if image1:
                image1_action = 'update'
            elif not image1 and not temp1:
                image1_action = 'delete'
            else:
                image1_action = 'none'

            if image2:
                image2_action = 'update'
            elif not image2 and not temp2:
                image2_action = 'delete'
            else:
                image2_action = 'none'

            if image3:
                image3_action = 'update'
            elif(not image3 and not temp3):
                image3_action = 'delete'
            else:
                image3_action = 'none'

            if image4:
                image4_action = 'update'
            elif(not image4 and not temp4):
                image4_action = 'delete'
            else:
                image4_action = 'none'

            if image5:
                image5_action = 'update'
            elif not image5 and not temp5:
                image5_action = 'delete'
            else:
                image5_action = 'none'

            images = {
                'image1': image1,
                'image2': image2,
                'image3': image3,
                'image4': image4,
                'image5': image5
            }

            actions = {
                'image1': image1_action,
                'image2': image2_action,
                'image3': image3_action,
                'image4': image4_action,
                'image5': image5_action
            }

            update = ItemImage.objects.get(item=Item.objects.get(id=request.GET.get('id', None)))

            if actions['image1'] == 'update':
                update.image1 = images['image1']
            elif actions['image1'] == 'delete':
                update.image1 = None

            if actions['image2'] == 'update':
                update.image2 = images['image2']
            elif actions['image2'] == 'delete':
                update.image2 = None

            if actions['image3'] == 'update':
                update.image3 = images['image3']
            elif actions['image3'] == 'delete':
                update.image3 = None

            if actions['image4'] == 'update':
                update.image4 = images['image4']
            elif actions['image4'] == 'delete':
                update.image4 = None

            if actions['image5'] == 'update':
                update.image5 = images['image5']
            elif actions['image5'] == 'delete':
                update.image5 = None

            update.save()

            pics = []

            update = ItemImage.objects.get(item=Item.objects.get(id=request.GET.get('id', None)))

            if update.image1: pics.append(update.image1)
            if update.image2: pics.append(update.image2)
            if update.image3: pics.append(update.image3)
            if update.image4: pics.append(update.image4)
            if update.image5: pics.append(update.image5)

            if len(pics)>=1:
                update.image1 = pics.pop(0)
            else:
                update.image1 = None

            if len(pics)>=1:
                update.image2 = pics.pop(0)
            else:
                update.image2 = None

            if len(pics)>=1:
                update.image3 = pics.pop(0)
            else:
                update.image3 = None

            if len(pics)>=1:
                update.image4 = pics.pop(0)
            else:
                update.image4 = None

            if len(pics)>=1:
                update.image5 = pics.pop(0)
            else:
                update.image5 = None

            update.save()

        return redirect('/profile')

    else:
        if request.user.is_authenticated():
            item = Item.objects.get(id=request.GET.get('id', None))
            if request.user == item.user:
                item_images = ItemImage.objects.get(item=item)
                form = ClosetItem(instance=item)
                photos = ClosetItemPhotos(instance=item_images)
                return render(request, 'slug_trade_app/add_closet_item.html', {'form': form, 'photos': photos, 'id': item_images.id, 'edit': True, 'images': item_images, 'item_id': item.id})
            else:
                return HttpResponse("You can't edit someone else's items.")
        else:
            return render(request, 'slug_trade_app/not_authenticated.html')

@csrf_exempt
def delete_closet_item(request):
    item = Item.objects.get(id=request.POST['item_id'])
    item_images = ItemImage.objects.get(item=item)
    item_images.delete()
    item.delete()
    return HttpResponse('Deleted!')

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
                return redirect('/home')
        else:
            return render(request, 'slug_trade_app/signup.html', {'user_form': user_form, 'profile_form': profile_form})

    else:
        user_form = UserForm()
        profile_form = SignupUserProfileForm()

        return render(request, 'slug_trade_app/signup.html', {'user_form': user_form, 'profile_form': profile_form})
