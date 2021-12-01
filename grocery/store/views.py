from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from datetime import datetime

from .models import *

from .utils import cookieCart, cartData, guestOrder

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required

#creating views here
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, CustomerForm, CommentForm
# Create your views here.

#import library
from recommended_products_pkg.recommended_products import RecommendedProduct

def registerPage(request):
    
    if request.user.is_authenticated:
        return redirect('store')
    
    else:
        
        form = CreateUserForm()
        
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account is created for '+ user)
                print(user)
                return redirect('login')
                
        
        context={'form': form}
        return render(request, 'store/register.html', context)


def loginPage(request):
    
    if request.user.is_authenticated:
        return redirect('store')
    
    else:
        
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, 'Username or Password is Incorrect')
                
            
        
        context={}
        return render(request, 'store/login.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User logged out')
    return redirect('login')



def details(request, pk):
    
    product=Product.objects.get(id=pk)
    
    num_comments = Comment.objects.filter(product=product).count()
    
    context={'product': product, 'num_comments':num_comments}
    return render(request, 'store/details.html', context)

def add_comment(request, pk):
    product = Product.objects.get(id=pk)
    
    form = CommentForm(instance=product)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=product)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['commenter_body'];
            c = Comment(product=product, commenter=name, commenter_body=body, date_added=datetime.now())
            c.save()
            return redirect('store')
        else:
            print('form is invalid')    
    else:
        form = CommentForm()    

    context = {
        'form': form
    }
    return render(request, 'store/add_comment.html', context)



def profile(request):
    print("profile")
    customer= request.user.customer
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    
    context={'form': form}
    return render(request, 'store/profile.html', context)



def store(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    
    
    
    products=Product.objects.all()
    
    context={'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    
    
    
    products=Product.objects.all()
    
    listId=[]
    for i in products:
        
        #product=Product.objects.get(id=1).id
        listId.append(i.id)
    print(listId, len(listId))
    #print(Product._meta.pk.name)
   
    n= RecommendedProduct()
    randNum=n.generate_random(len(listId))
    print('Random number:{}'.format(randNum))
    
    #recommended_product=0
 
    recommended_product=Product.objects.get(id=listId[randNum-1])
    print(recommended_product)
    
  
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
        
    context={'items':items , 'order': order, 'cartItems': cartItems, 'recommended_product':recommended_product}
    return render(request, 'store/cart.html', context)




def checkout(request):
    
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
        
    context={'items':items , 'order': order, 'cartItems': cartItems}
    
    return render(request, 'store/checkout.html', context)
    
    
def updateItem(request):
    data=json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('ProductId:', productId)
    
    
    customer= request.user.customer
    product=Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
        
    elif action =='remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return JsonResponse('Item was added', safe=False)
    
    
def processOrder(request):
    
    transaction_id = datetime.datetime.now().timestamp()
    
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
        
        
    else:
        customer, order = guestOrder(request, data)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
        
    if total == float(order.get_cart_total):
        order.complete= True
    order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
            
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            county=data['shipping']['state'],
            eircode=data['shipping']['zipcode'],

        )
    
    
    
    return JsonResponse('Payment complete!', safe=False)
    