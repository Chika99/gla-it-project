from django import forms
from django.contrib.auth.forms import AuthenticationForm

from app.models import User, Order, Bid, Message


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'avatar', 'tel', 'balance', 'credit_level', 'address']


class OrderForm(forms.ModelForm):
    end_time = forms.DateTimeField(widget=forms.DateTimeInput())

    class Meta:
        model = Order
        fields = ['title', 'description', 'start_price', 'end_time']


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
