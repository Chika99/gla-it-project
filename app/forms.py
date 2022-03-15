from django import forms

from app.models import User, Order, Bid, Message, Comment


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    tel = forms.IntegerField(required=False)
    balance = forms.FloatField(required=False)
    credit_level = forms.IntegerField(required=False)
    address = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'avatar', 'tel', 'balance', 'credit_level', 'address']


class OrderForm(forms.ModelForm):
    end_time = forms.DateTimeField(widget=forms.DateTimeInput())
    start_price = forms.FloatField()

    class Meta:
        model = Order
        fields = ['title', 'description', 'start_price', 'end_time']


class BidForm(forms.ModelForm):
    price = forms.FloatField()

    class Meta:
        model = Bid
        fields = ['price']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['rate', 'content']
