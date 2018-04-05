from django.shortcuts import render

# Create your views here.

def index(request):
    test = "This was passed from the backend!"
    print("in index view")
    return render(request, 'slug_trade_app/index.html',{'test':test})

def products(request):
    return render(request, 'slug_trade_app/products.html')
