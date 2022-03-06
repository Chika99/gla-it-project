from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User as UserModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(upload_to='user_avatar', blank=True, null=True)
    tel = models.IntegerField(blank=True, null=True)
    balance = models.IntegerField(default=0)
    credit_level = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username


class Order(models.Model):
    STATUS = (('U', 'PUBLISH'), ('F', 'FINISH'), ('C', 'CANCEL'),)
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='buyer')
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    start_price = models.IntegerField(validators=[MinValueValidator(1)])
    publish_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS, default='U')


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    orders = models.ManyToManyField(Order)


class OrderImage(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='order_images')


class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now=True)


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
