from django.urls import path

from app import views

app_name = 'app'

urlpatterns = [
    path('', views.order_list, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('my/', views.my, name='my'),
    path('add_order/', views.add_order, name='add_order'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/add_bid/', views.add_bid, name='add_bid'),
    path('orders/<int:order_id>/add_message/', views.add_message, name='add_message'),
    path('orders/<int:order_id>/<int:message_id>/reply/', views.reply_message, name='reply_message'),
]
