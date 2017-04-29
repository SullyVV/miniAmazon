from django.conf.urls import url, include
from django.contrib.auth import authenticate

from .registration.backends.simple.views import RegistrationView
from . import views
app_name = 'amazon'
class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return "/amazon/"
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
    #/amazon/history/5
    url(r'^history/(?P<user_id>[0-9]+)/$', views.history, name='history'),
    #/amazon/catalog/1
    url(r'^catalog/(?P<catalog_id>[0-9]+)/$', views.catalog, name='catalog'),
    #/amazon/search
    url(r'^search/$', views.search, name='search'),
    #/amazon/put_order/1
    url(r'^put_order/(?P<product_id>[0-9]+)/$', views.put_order, name='put_order'),
    #/user/admin,
    url(r'^user/(?P<userid>[0-9]+)/$', views.user, name='user'),
]