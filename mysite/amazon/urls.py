from django.conf.urls import url, include
from django.contrib.auth import authenticate

from .registration.backends.simple.views import RegistrationView
from . import views
app_name = 'amazon'
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return "/amazon/"

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return "/amazon/"

    def register(self, form):
        new_user = form.save()
        print("in new class")
        return new_user
urlpatterns = [
    #/amazon/
    url(r'^$', views.index, name='index'),
    #/amazon/register/,
    url(r'^accounts/register/', MyRegistrationView.as_view(), name='registration_register'),
    #/login/,
    url(r'^accounts/login/$', views.login, name='login'),
    #/logout/,
    url(r'^accounts/logout/$', views.logout, name='logout'),
    #/buy/,
    url(r'^product/$', views.buy, name='product'),
    #/user/admin,
    url(r'^user/(?P<userid>[0-9]+)/$', views.user, name='user'),
]