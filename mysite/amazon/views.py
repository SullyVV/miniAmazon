import threading

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.urls import reverse

from .client import Client
from .forms import UserForm_login, ProductForm, SearchForm
from .models import Whstock, Transaction

users = {}
threads = {}
ship_id = 0

def index(request):
    return render(request, 'amazon/index.html')

def login(request):
    if (request.method == 'POST'):
        uf = UserForm_login(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request,user)
                userid = User.objects.get(username=username).id
                # create Client object for this client
                client = Client()
                client.connect()
                client.AConnect()
                users[userid] = client
                threads[userid] = threading.Thread(target=client.process_AResponse)
                threads[userid].start()
                return HttpResponseRedirect(reverse('amazon:user',args=(userid,)))
            else:
                error_msg = "Wrong password, please try again"
                return render_to_response('amazon/login.html', {'uf': uf, 'error_msg': error_msg})
    else:
        uf = UserForm_login()
    return render(request, 'amazon/login.html', {'uf':uf})

def logout(request):
    # need to kill this thread before pop up map
    threads.pop(request.user.id)
    users.pop(request.user.id)
    auth_logout(request)
    return HttpResponseRedirect(reverse('amazon:index'))

def buy(request):
    if request.method == "POST":
        uf = ProductForm(request.POST)
        if uf.is_valid():
            pid = uf.cleaned_data['pid']
            dsc = uf.cleaned_data['dsc']
            num = uf.cleaned_data['num']
            addr_x = uf.cleaned_data['x']
            addr_y = uf.cleaned_data['y']
            products = Whstock.objects.filter(dsc = dsc).filter(pid = pid).filter(count__gte = num)
            client = users[request.user.id]
            if len(products) != 0:
                # accept this order
                global ship_id
                trans = Transaction()
                trans.user = request.user
                trans.user_name = request.user.username
                trans.stock = products[0]
                trans.product_name = dsc
                trans.product_num = num
                trans.address_x = addr_x
                trans.address_y = addr_y
                trans.ship_id = ship_id
                trans.arrived = True
                trans.save()
                products[0].count = products[0].count - num
                products[0].save()
                client.AToPack(products[0].pid, products[0].dsc, num, ship_id)
                ship_id = ship_id + 1
                return render(request, 'amazon/order_accepted.html', {'user_id':request.user.id})
            else:
                # deny order and tell warehouse to import
                client.APurchase(pid, dsc, num)
                return render(request, 'amazon/product.html', {'uf': uf, 'error_msg': 'Your order is rejected (no sufficient stock), Plz try again later...'})
    else:
        uf = ProductForm()
    return render(request, 'amazon/product.html', {'uf':uf})

def put_order(request, product_id):
    product = get_object_or_404(Whstock, pid=product_id)
    print(product)
    if request.method == "POST":
        pf = ProductForm(request.POST)
        if pf.is_valid():
            order_num = pf.cleaned_data['order_num']
            addr_x = pf.cleaned_data['x']
            addr_y = pf.cleaned_data['y']
            ups_act = pf.cleaned_data['ups_act']
            print(ups_act)
            client = users[request.user.id]
            if order_num <= product.count:
                # accept this order
                global ship_id
                trans = Transaction()
                trans.user = request.user
                trans.user_name = request.user.username
                trans.stock = product
                trans.product_name = product.dsc
                trans.product_num = order_num
                if ups_act is not None:
                    trans.ups_act = ups_act
                trans.address_x = addr_x
                trans.address_y = addr_y
                trans.ship_id = ship_id
                trans.arrived = True
                trans.save()
                product.count = product.count - order_num
                product.save()
                client.AToPack(product.pid, product.dsc, order_num, ship_id)
                ship_id = ship_id + 1
                return render(request, 'amazon/order_accepted.html', {'user_id':request.user.id})
            else:
                # deny order and tell warehouse to import
                client.APurchase(product.pid, product.dsc, order_num - product.count)
                return render(request, 'amazon/put_order.html', {'pf': pf, 'product':product, 'error_msg': 'Your order is rejected (no sufficient stock), Plz try again later...'})
    else:
        pf = ProductForm()
    return render(request, 'amazon/put_order.html', {'pf':pf, 'product':product})

def user(request, userid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('amazon:login'))
    user = get_object_or_404(User, pk=userid)
    return render(request, 'amazon/user.html',
                    {'user': user})
    # show all event of current user and put a plus button for it to add new event, traverse through entire database and show events

def history(request, user_id):
    # show transactions history
    print("show history for user: " + user_id)
    trans = Transaction.objects.filter(user = request.user)
    return render(request, 'amazon/history.html', {'trans':trans})

def catalog(request, catalog_id):
    products = Whstock.objects.filter(ctlg_id=catalog_id)
    return render(request, 'amazon/catalog.html', {'products': products})

def search(request):
    if (request.method == 'POST'):
        sf = SearchForm(request.POST)
        if sf.is_valid():
            catalog = sf.cleaned_data['catalog']
            name = sf.cleaned_data['name']
            print(catalog)
            print(name)
            products = Whstock.objects.filter(pid = -1)
            if catalog is not '':
                products = Whstock.objects.filter(ctlg=catalog)
            elif name is not '':
                products = Whstock.objects.filter(dsc=name)
            if len(products) != 0:
                return render(request, 'amazon/search_result.html', {'flag':0, 'products': products})
            else :
                return render(request, 'amazon/search_result.html', {'flag':1, 'error_msg': "no products"})

    else:
        sf = SearchForm()
    return render(request, 'amazon/search.html', {'sf':sf})