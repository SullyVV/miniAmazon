from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User


# Create your views here.
from django.urls import reverse

from .forms import UserForm_login


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
                return HttpResponseRedirect(reverse('amazon:user',args=(userid,)))
            else:
                error_msg = "Wrong password, please try again"
                return render_to_response('amazon/login.html', {'uf': uf, 'error_msg': error_msg})
    else:
        uf = UserForm_login()
    return render(request, 'amazon/login.html', {'uf':uf})

def logout(request):
    auth_logout(request)
    # redirect to index page
    return HttpResponseRedirect(reverse('amazon:index'))

def buy(request):
    print("in buy function")

def user(request, userid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('rsvp:login'))
    user = get_object_or_404(User, pk=userid)
    return render(request, 'amazon/user.html',
                    {'user': user})
    # show all event of current user and put a plus button for it to add new event, traverse through entire database and show events
