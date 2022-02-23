import os

import tzlocal
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth.views import LoginView
from django.urls import path
from django_apscheduler.jobstores import DjangoJobStore

from app import views
from app.views import RegisterView, OrderView, OrderDetailView, UserDetailView, AddOrderView, AddBidFormView, \
    AddMessageFormView, ReplyMessageFormView, check_order, CommentFormView

app_name = 'app'

urlpatterns = [
    path('', OrderView.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='app/login.html', next_page='app:index'), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/<int:user_id>', UserDetailView.as_view(), name='user'),
    path('add_order/', AddOrderView.as_view(), name='add-order'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:order_id>/add_bid/', AddBidFormView.as_view(), name='add-bid'),
    path('orders/<int:order_id>/add_message/', AddMessageFormView.as_view(), name='add-message'),
    path('orders/<int:order_id>/<int:message_id>/reply/', ReplyMessageFormView.as_view(), name='reply-message'),
    path('orders/<int:order_id>/comment', CommentFormView.as_view(), name='add-comment')
]

env_dist = os.environ

if not env_dist.get('init'):
    scheduler = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))
    scheduler.add_jobstore(DjangoJobStore(), 'default')


    @scheduler.scheduled_job('interval', id='check_order', seconds=10)
    def order_job():
        check_order()


    scheduler.start()
