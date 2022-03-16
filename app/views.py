import logging
import time

from PIL import Image
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView, DetailView

from app.dtos import OrderDto, OrderDetailDto, UserDetailDto
from app.forms import RegisterForm, OrderForm, BidForm, MessageForm, CommentForm, UserModifyForm
from app.models import Tag, OrderImage, Order, Message, Bid, User, Comment


class RegisterView(FormView):
    template_name = 'app/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.balance = round(user.balance, 2) * 100
        user.set_password(user.password)
        if 'avatar' in self.request.FILES:
            user.avatar = self.request.FILES['avatar']
        user.save()
        HttpResponse("<script>alert('Create account successfully!')</script>") 
        # todo
        return HttpResponseRedirect(reverse('app:login'))

    def form_invalid(self, form):
        return self.render_to_response({'form': form})


class OrderView(ListView):
    template_name = 'app/index.html'
    model = OrderDto
    paginate_by = 10
    page_kwarg = 'page'

    def get_queryset(self):
        query_set = None

        tags = self.request.GET.getlist('tags', [])
        for i in tags:
            s = Order.objects.filter(tag__name=i)
            query_set = query_set | s if query_set else s

        keywords = self.request.GET.get('keywords')
        if keywords:
            s = Order.objects.filter(title__contains=keywords) | Order.objects.filter(description__contains=keywords)
            query_set = query_set & s if query_set else s

        ref = {
            'publish_time': 'publish_time',
            'end_time': 'end_time',
        }

        # 只允许一个排序
        for i in ref:
            if i in self.request.GET.dict():
                s = Order.objects.order_by(f'-{ref[i]}' if self.request.GET.get(i) == 'desc' else ref[i])
                query_set = query_set & s if query_set else s
                break

        self.paginate_by = self.request.GET.get('size', 10)

        return Order.objects.all() if query_set is None else query_set

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = [OrderDto(order) for order in context['object_list']]
        context['size'] = self.paginate_by
        return context


class OrderDetailView(DetailView):
    template_name = 'app/order_detail.html'
    model = OrderDetailDto
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    def get_queryset(self):
        return Order.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = OrderDetailDto(context['order'])
        return context


# Modify Order
@login_required
def orderModify(request, id):
    # If the request method is GET, then render to order_modify.html
    if request.method == 'GET':
        oData = Order.objects.get(id=id)
        return render(request, "app/order_modify.html", {"data": oData})

    # If the request method is POST, then modify here
    # Match the corresponding modifications to complete the modification of the order
    if request.method == 'POST':
        data = {}
        data["title"] = request.POST["title"]
        data["description"] = request.POST["description"]
        data["start_price"] = request.POST["start_price"]
        data["end_time"] = str(request.POST["end_time"])
        o = Order.objects.get(id=id)
        o.title = data["title"]
        o.description = data['description']
        o.start_price = data["start_price"]
        o.end_time = data["end_time"]
        o.save()

        if request.FILES.getlist('images'):
            o.orderimage_set.all().delete()
        o.tag_set.all().delete()

        for i in request.POST.getlist('tags'):
            tag = Tag.objects.get_or_create(name=i)[0]
            tag.orders.add(o)
            tag.save()

        for i in request.FILES.getlist('images'):
            try:
                img = Image.open(i)
                img.verify()
            except:
                return "1"
            image = OrderImage(img=i)
            image.order = o
            image.save()
        return HttpResponseRedirect("/")


# Cancel the order
@login_required
def orderModifyStatus(request, id):
    # Click the cancel button to modify the decoration of the order to C (i.e., cancel)
    o = Order.objects.get(id=id)
    o.status = 'C'
    o.save()
    return HttpResponse("<script>alert('Order cancelled successfully');history.go(-1)</script>")


class UserDetailView(DetailView):
    template_name = 'app/user_detail.html'
    model = UserDetailDto
    context_object_name = 'user_info'
    pk_url_kwarg = 'user_id'

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs.get(self.pk_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_info'] = UserDetailDto(context['user_info'])
        return context


@method_decorator(login_required, name='dispatch')
class AddOrderView(FormView):
    template_name = 'app/add_order.html'
    form_class = OrderForm

    def form_valid(self, form):
        order = form.instance
        if order.end_time < timezone.now():
            return self.render_to_response({
                'form': form,
                'added': False,
                'message': 'end time should in future',
            })
        order.start_price = round(order.start_price, 2) * 100
        order = form.save(commit=False)
        order.seller = self.request.user
        order.save()
        for i in self.request.POST.getlist('tags'):
            tag = Tag.objects.get_or_create(name=i)[0]
            tag.orders.add(order)
            tag.save()
        for i in self.request.FILES.getlist('images'):
            try:
                img = Image.open(i)
                img.verify()
            except:
                return self.render_to_response({
                    'form': form,
                    'added': False,
                    'message': 'invalid image',
                })
            image = OrderImage(img=i)
            image.order = order
            image.save()
        return self.render_to_response({
            'added': True
        })

    def form_invalid(self, form):
        return self.render_to_response({'form': form})


# 提供order_id注入get和form上下文, 继承使用
class OrderRelatedFormView(FormView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_id'] = self.kwargs.get('order_id')
        return context

    def response(self, form, message, added: bool, **kwargs):
        return self.render_to_response({
                                           'form': form,
                                           'message': message,
                                           'added': added,
                                           'order_id': self.kwargs.get('order_id')
                                       } | kwargs)


@method_decorator(login_required, name='dispatch')
class AddBidFormView(OrderRelatedFormView):
    template_name = 'app/add_bid.html'
    form_class = BidForm

    def form_valid(self, form):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        bid = form.instance
        bid.price = round(bid, 2) * 100
        balance = self.request.user.balance

        def bad_request(message):
            return self.response(form, message, False)

        if order.seller.id == self.request.user.id:
            return bad_request('cannot bid own order')
        if timezone.now() > order.end_time:
            return bad_request('order has finished')
        if bid.price < order.start_price:
            return bad_request('bid is lower than start price')

        last_highest_bid = Bid.objects.filter(order__id=order.id).order_by('-price').first()
        if last_highest_bid and bid.price < last_highest_bid.price:
            return bad_request('bid is lower than highest price')

        # 如果有上次赌注
        last_bid = Bid.objects.filter(user__id=self.request.user.id, order__id=order.id).order_by('-price').first()
        price_diff = (bid.price - last_bid.price) if last_bid else bid.price
        if price_diff > balance:
            return bad_request('balance not enough')

        bid = form.save(commit=False)
        bid.user = self.request.user
        bid.order = order
        bid.save()

        self.request.user.balance = balance - price_diff
        self.request.user.save()
        return self.response(None, None, True)


@method_decorator(login_required, name='dispatch')
class AddMessageFormView(OrderRelatedFormView):
    template_name = 'app/add_message.html'
    form_class = MessageForm

    def form_valid(self, form):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        message = form.save(commit=False)
        message.order = order
        message.user = self.request.user
        message.save()
        return self.response(None, None, True)

    def form_invalid(self, form):
        return self.response(MessageForm(), None, False)


@method_decorator(login_required, name='dispatch')
class ReplyMessageFormView(OrderRelatedFormView):
    template_name = 'app/add_message.html'
    form_class = MessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reply'] = get_object_or_404(Message, id=self.kwargs.get('message_id'))
        return context

    def form_valid(self, form):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        reply = get_object_or_404(Message, id=self.kwargs.get('message_id'))
        message = form.save(commit=False)
        message.order = order
        message.reply = reply
        message.user = self.request.user
        message.save()
        return self.response(None, None, True)

    def form_invalid(self, form):
        reply = get_object_or_404(Message, id=self.kwargs.get('message_id'))
        return self.response(MessageForm(), None, False, reply=reply)


@method_decorator(login_required, name='dispatch')
class CommentFormView(OrderRelatedFormView):
    template_name = 'app/add_comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        if not order.status == 'F':
            return self.response(form, 'cannot comment on unfinished order', False)
        # request user id
        r_id = self.request.user.id
        if r_id == order.seller.id:
            ex_comment = Comment.objects.filter(Q(order__id=order.id, user__id=r_id) & Q(order__seller_id=r_id))
        elif self.request.user.id == order.buyer.id:
            ex_comment = Comment.objects.filter(Q(order__id=order.id, user__id=r_id) & Q(order__buyer_id=r_id))
        else:
            return self.response(form, 'cannot comment on unrelated order', False)

        if ex_comment.first():
            return self.response(form, 'already comment', False)
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.order = order
        comment.save()
        return self.response(None, None, True)

    def form_invalid(self, form):
        return self.response(CommentForm(), None, False)


@login_required
def logout(request):
    user_logout(request)
    return redirect(reverse('app:index'))


def check_order():
    # 正在出售的订单
    for order in Order.objects.filter(status='U'):
        if order.end_time <= timezone.now():
            logger = logging.getLogger(__name__)
            user_bid = {
                user: Bid.objects.filter(user__id=user.id, order__id=order.id).order_by('-price').first()
                for user in User.objects.filter(bid__order__id=order.id).distinct()
            }
            first = False
            for (user, bid) in sorted(user_bid.items(), key=lambda i: i[1].price, reverse=True):
                if not first:
                    order.seller.balance += bid.price
                    order.seller.save()
                    order.buyer = user
                    order.status = 'F'
                    order.save()
                    logger.warning(f'seller user:{order.seller.id} get deal:{bid.price}')
                    first = True
                else:
                    user.balance += bid.price
                    logger.warning(f'user:{user.id} get returned bid:{bid.price}')
                    user.save()
            # 没有人买
            if not first:
                order.status = 'C'
                order.save()
                logger.warning(f'order:{order.id} has cancelled because of no bid')
            else:
                logger.warning(f'order:{order.id} has settled')

def user_modify(request, **kwargs):
    user = User.objects.get(username=request.user.username)

    if request.method == "POST":
        user_form = UserModifyForm(request.POST)
        if user_form.is_valid():
            user_modify = user_form.cleaned_data
            # user.avatar = user_modify['avatar']
            user.username = user_modify['username']
            user.tel = user_modify['tel']
            user.address = user_modify['address']
            # avatar = request.POST['avatar']
            # user.avatar = avatar

            user.save()
        return redirect(reverse('app:index'))
    else:
        user_form = UserModifyForm(instance=request.user)
        return render(request, "app/user_modify.html", {"user_form":user_form})
