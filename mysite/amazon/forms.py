from django import forms


class UserForm_login(forms.Form):
    username = forms.CharField(label="username", max_length=100)
    password = forms.CharField(label="password", widget=forms.PasswordInput)

class ProductForm(forms.Form):
    pid = forms.IntegerField(label="product_id")
    dsc = forms.CharField(label="product_description")
    num = forms.IntegerField(label="product_count")