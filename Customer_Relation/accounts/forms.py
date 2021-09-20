from django import  forms
from django.contrib.auth.forms import UserCreationForm
from .models import Order
from  django.contrib.auth.models import User
from .models import Customer

class orderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateuserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
