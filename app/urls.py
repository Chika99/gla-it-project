from django.contrib.auth.views import LoginView
from django.urls import path

from app import views
from app.views import RegisterView, OrderView, OrderDetailView, UserDetailView, AddOrderView, AddBidFormView, \
    AddMessageFormView, ReplyMessageFormView, CommentFormView

app_name = 'app'

urlpatterns = [
    # Homepage, the orders' view
    path('', OrderView.as_view(), name='index'),
    # Login
    path('login/', LoginView.as_view(template_name='app/login.html', next_page='app:index'), name='login'),
    # Logout
    path('logout/', views.logout, name='logout'),
    # Register
    path('register/', RegisterView.as_view(), name='register'),
    # User's centre
    path('user/<int:user_id>', UserDetailView.as_view(), name='user'),
    # Add a new order
    path('add_order/', AddOrderView.as_view(), name='add-order'),
    # Show the orders' detail
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    # Add bid
    path('orders/<int:order_id>/add_bid/', AddBidFormView.as_view(), name='add-bid'),
    # Add new massage
    path('orders/<int:order_id>/add_message/', AddMessageFormView.as_view(), name='add-message'),
    # Reply massage
    path('orders/<int:order_id>/<int:message_id>/reply/', ReplyMessageFormView.as_view(), name='reply-message'),
    # Add comments - when received the goods, not used now
    path('orders/<int:order_id>/comment', CommentFormView.as_view(), name='add-comment'),
    # Order modification
    path("ordermodify/<id>", views.orderModify, name="orderModify"),
    # Cancel order
    path("ordermodifystatus/<id>", views.orderModifyStatus, name="orderModifyStatus"),
    # modify user's information
    path('user_modify/<int:user_id>', views.user_modify, name='user_modify'),
]

# env_dist = os.environ
#
# if not env_dist.get('init'):
#     scheduler = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))
#     scheduler.add_jobstore(DjangoJobStore(), 'default')
#
#
#     @scheduler.scheduled_job('interval', id='check_order', seconds=10)
#     def order_job():
#         check_order()
#
#
#     scheduler.start()
