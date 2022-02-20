from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from app.dtos import OrderDto, MessageDto, BidDto
from app.forms import UserForm, OrderForm, BidForm, MessageForm
from app.models import Tag, OrderImage, Order, Message, Bid


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            user_login(request, user)
            return redirect(reverse('app:index'))
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Incorrect username or password")
    else:
        return render(request, 'app/login.html')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']

            user.save()
            registered = True
        else:
            # todo handle logs
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request, 'app/register.html', context={
        'user_form': user_form,
        'registered': registered,
    })


def order_list(request):
    if request.method == 'GET':
        query_set = None

        tags = request.GET.getlist('tags', [])
        for i in tags:
            s = Order.objects.filter(tag__name=i)
            query_set = query_set | s if query_set else s

        keywords = request.GET.get('keywords', None)
        if keywords:
            s = Order.objects.filter(title__contains=keywords) | Order.objects.filter(description__contains=keywords)
            query_set = query_set & s if query_set else s

        time_order = request.GET.get('time_order', 'desc')
        s = Order.objects.order_by('publish_time')
        s = s.reverse() if time_order == 'desc' else s
        query_set = query_set & s if query_set else s

        end_time_order = request.GET.get('end_time_order', 'desc')
        s = Order.objects.order_by('end_time')
        s = s.reverse() if end_time_order == 'desc' else s
        query_set = query_set & s if query_set else s

        # todo 当前价格排序

        query_set = Order.objects.all() if query_set is None else query_set

        size = request.GET.get('size', 10)
        paginator = Paginator(query_set, size)
        page = paginator.get_page(request.GET.get('page', 1))
        # 这里转换成dto
        page.object_list = [OrderDto(order) for order in page.object_list]
        # print([o.title for o in page.__dict__['object_list']])
        return render(request, 'app/index.html', context={'page': page, 'size': size})

    return JsonResponse({'code': 405, 'message': 'Method Not Allowed'})


def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect(reverse('app:index'))
    msg_dto = [MessageDto(message) for message in Message.objects.filter(order__id=order_id)]
    bid_dto = [BidDto(bid) for bid in Bid.objects.filter(order__id=order_id).order_by('id').reverse()]
    dto = OrderDto(order)
    return render(request, 'app/order_detail.html', context={'order': dto, 'messages': msg_dto, 'bids': bid_dto})


@login_required
def logout(request):
    user_logout(request)
    return redirect(reverse('app:index'))


@login_required
def my(request):
    orders = Order.objects.filter(user__id=request.user.id)
    dto = [OrderDto(order) for order in orders]
    return render(request, 'app/my.html', context={'orders': dto})


@login_required
def add_order(request):
    added = False
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.instance
            if order.end_time < timezone.now():
                return render(request, 'app/add_order.html', context={
                    'order_form': order_form,
                    'added': added,
                    'message': 'end time should in future',
                })
            order = order_form.save(commit=False)
            order.user = request.user
            order.save()
            for i in request.POST.getlist('tags'):
                tag = Tag.objects.get_or_create(name=i)[0]
                tag.orders.add(order)
                tag.save()
            # todo image格式检测
            for i in request.FILES.getlist('images'):
                image = OrderImage(img=i)
                image.order = order
                image.save()
            added = True
        else:
            # todo handle log
            print(order_form.errors)
    else:
        order_form = OrderForm()
    return render(request, 'app/add_order.html', context={
        'order_form': order_form,
        'added': added,
        'message': '',
    })


@login_required
def add_bid(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect(reverse('app:index'))
    added = False

    def bad_request(message):
        return render(request, 'app/add_bid.html', context={
            'bid_form': BidForm(),
            'message': message,
            'added': False,
            'order_id': order_id
        })

    if request.method == 'POST':
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid = bid_form.instance
            balance = request.user.balance

            if timezone.now() > order.end_time:
                return bad_request('order has finished')
            if bid.price < order.start_price:
                return bad_request('bid is lower than start price')
            if bid.price > balance:
                return bad_request('balance not enough')
            if order.user.id == request.user.id:
                return bad_request('cannot bid own order')

            bid = bid_form.save(commit=False)
            bid.user = request.user
            bid.order = order
            bid.save()
            request.user.balance = balance - bid.price
            # fixme 这里要改规则
            # 如果有上次赌注，则返还
            last_bid = Bid.objects.filter(user__id=request.user.id, order__id=order_id).order_by(
                'price').reverse().first()
            if last_bid:
                request.user.balance = balance + last_bid.price
            request.user.save()
            added = True
        else:
            # todo handle log
            print(bid_form.errors)
    else:
        bid_form = BidForm()
    return render(request, 'app/add_bid.html', context={
        'bid_form': bid_form,
        'message': '',
        'added': added,
        'order_id': order_id
    })


@login_required
def add_message(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect(reverse('app:index'))
    added = False

    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.order = order
            message.user = request.user
            message.save()
            added = True
        else:
            print(message_form.errors)
    else:
        message_form = MessageForm()
    return render(request, 'app/add_message.html', context={
        'message_form': message_form,
        'added': added,
        'reply': '',
        'order_id': order_id
    })


@login_required
def reply_message(request, order_id, message_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return redirect(reverse('app:index'))

    try:
        reply = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return redirect(reverse('app:index'))

    added = False

    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.order = order
            message.user = request.user
            message.reply = reply
            message.save()
            added = True
        else:
            print(message_form.errors)
    else:
        message_form = MessageForm()
    return render(request, 'app/add_message.html', context={
        'message_form': message_form,
        'reply': MessageDto(reply),
        'added': added,
        'order_id': order_id
    })
