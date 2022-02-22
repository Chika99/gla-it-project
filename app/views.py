from PIL import Image
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView, DetailView

from app.dtos import OrderDto, OrderDetailDto, UserDetailDto
from app.forms import RegisterForm, OrderForm, BidForm, MessageForm
from app.models import Tag, OrderImage, Order, Message, Bid, User


class RegisterView(FormView):
    template_name = 'app/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        if 'avatar' in self.request.FILES:
            user.avatar = self.request.FILES['avatar']
        user.save()
        # todo 这里可以跳转成功页面/login页面带信息
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
        order = form.save(commit=False)
        order.user = self.request.user
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
class OrderRelatedView(FormView):

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
class AddBidView(OrderRelatedView):
    template_name = 'app/add_bid.html'
    form_class = BidForm

    def form_valid(self, form):
        order = get_object_or_404(Order, id=self.kwargs.get('order_id'))
        bid = form.instance
        balance = self.request.user.balance

        def bad_request(message):
            return self.response(form, message, False)

        if order.user.id == self.request.user.id:
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
class AddMessageView(OrderRelatedView):
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
class ReplyMessageView(OrderRelatedView):
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


@login_required
def logout(request):
    user_logout(request)
    return redirect(reverse('app:index'))
