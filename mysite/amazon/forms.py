from django import forms


class UserForm_login(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", widget=forms.PasswordInput)

class ProductForm(forms.Form):
    order_num = forms.IntegerField(label="quantity")
    x = forms.IntegerField(label="address_x (prefilled with default address)")
    y = forms.IntegerField(label="address_y (prefilled with default address)")
    ups_act = forms.IntegerField(label="UPS Account number (prefilled with default UPS Account)", required=False)

class SearchForm(forms.Form):
    catalog = forms.CharField(label="search for catalog", required=False)
    name = forms.CharField(label="search for product name", required=False)


class UserInfoForm(forms.Form):
    address_x = forms.IntegerField(label="address_x", required=False)
    address_y = forms.IntegerField(label="address_y", required=False)
    ups_act = forms.IntegerField(label="ups account number", required=False)
