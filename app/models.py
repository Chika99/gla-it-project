from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User as UserModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# User class
class User(AbstractUser):
    # User id
    id = models.AutoField(primary_key=True)
    # User name
    username = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(upload_to='user_avatar', blank=True, null=True)
    # User's telephone number
    tel = models.IntegerField(blank=True, null=True)
    # User's money in this website
    balance = models.IntegerField(default=0)
    # User's credit level. Multiple trades and good reviews will improve this
    credit_level = models.IntegerField(blank=True, null=True)
    # User's address
    address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username


# Order class
class Order(models.Model):
    # Each order has 3 status: U means published, F means finished the bargain, c means cancel the release.
    STATUS = (('U', 'PUBLISH'), ('F', 'FINISH'), ('C', 'CANCEL'),)
    # Order id
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='buyer')
    # Title of this order
    title = models.CharField(max_length=50)
    # Description of this order
    description = models.CharField(max_length=200)
    # The lowest price of the goods from seller
    start_price = models.IntegerField(validators=[MinValueValidator(1)])
    publish_time = models.DateTimeField(auto_now=True)
    # When does the deal have to go through
    end_time = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS, default='U')


# The tag of goods class
class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    # Which orders have this label
    orders = models.ManyToManyField(Order)


# The images of orders class
class OrderImage(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='order_images')


# The bid class
class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    time = models.DateTimeField(auto_now=True)


# The comment of goods class
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now=True)


# The message of goods class
class Message(models.Model):
    # The message id
    id = models.AutoField(primary_key=True)
    # The message of which order
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # The message from who
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The content of message
    content = models.CharField(max_length=200)
    # Message time
    time = models.DateTimeField(auto_now=True)
    # The reply of the message
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
