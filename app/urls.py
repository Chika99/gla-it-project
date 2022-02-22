from django.contrib.auth.views import LoginView
from django.urls import path

from app import views
from app.views import RegisterView, OrderView, OrderDetailView, UserDetailView, AddOrderView, AddBidView, \
    AddMessageView, ReplyMessageView

app_name = 'app'

urlpatterns = [
    path('', OrderView.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='app/login.html', success_url=''), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/<int:user_id>', UserDetailView.as_view(), name='user'),
    path('add_order/', AddOrderView.as_view(), name='add_order'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:order_id>/add_bid/', AddBidView.as_view(), name='add_bid'),
    path('orders/<int:order_id>/add_message/', AddMessageView.as_view(), name='add_message'),
    path('orders/<int:order_id>/<int:message_id>/reply/', ReplyMessageView.as_view(), name='reply_message'),
]
