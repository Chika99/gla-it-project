import os
import random

from django.utils.timezone import make_aware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction.settings')

import django

django.setup()
from faker import Faker
from app.models import User, Order, OrderImage, Bid, Message

f = Faker()

orders_dict = {
    'badminton': 1,
    'bag': 2,
    'bike': 2,
    'book': 2,
    'clothes': 1,
    'computer': 1,
    'hat': 2,
    'keyboard': 2,
    'laptop': 2,
    'mouse': 2,
    'necklace': 3,
    'painting': 2,
    'shoes': 2
}

orders = []
for k in orders_dict:
    if orders_dict[k] > 1:
        for i in range(orders_dict[k]):
            orders.append(f'{k}{i + 1}')
    else:
        orders.append(f'{k}{orders_dict[k]}')


def get_users():
    users = [{'username': 'admin', 'password': 'admin', 'balance': 1000000, 'avatar': 'user_avatar/admin.png'}]
    names = [f.unique.first_name() for _ in range(12)]
    for i in range(12):
        users.append({
            'username': names[i],
            'password': 'password',
            'balance': 1000000,
            'avatar': f'user_avatar/avatar{i}.png',
            'tel': int(f'{f.random_int()}{f.random_int()}'),
            'address': f.address(),
        })
    return users


added_users = []
added_orders = []


def populate():
    for user in get_users():
        add_user_and_order(user)
    add_bid()
    add_message()


def add_user_and_order(user):
    # create user
    u = User.objects.create_user(**user)
    u.save()
    if u.username == 'admin':
        return
    added_users.append(u)
    # create order
    for _ in range(2):
        o = orders.pop(0)
        if not o:
            break
        oo = Order.objects.create(
            **{
                'title': o,
                'description': f'this is a {o} description',
                'start_price': f.random_int(),
                'end_time': make_aware(f.future_date()),
                'seller': u,
            })
        oo.save()
        added_orders.append(oo)
        # save images
        for _ in range(random.randint(1, 3)):
            img = OrderImage.objects.create(img=f'order_images/{o}.jpg', order=oo)
            img.save()


def add_bid():
    for o in added_orders:
        start_price = o.start_price
        # users which are not seller
        us = [u for u in filter(lambda user: not user.id == o.id, added_users)]
        for _ in range(random.randint(1, 5)):
            start_price += random.randint(100, 10000)
            u = random.choice(us)
            b = Bid.objects.create(price=start_price, order=o, user=u)
            b.save()


def add_message():
    for o in added_orders:
        added_message = [None]
        for _ in range(random.randint(1, 5)):
            u = random.choice(added_users)
            m = Message.objects.create(
                content=f.text(max_nb_chars=50),
                reply=random.choice(added_message),
                user=u,
                order=o
            )
            m.save()
            added_message.append(m)


if __name__ == '__main__':
    print('Starting population script...')
    populate()
    print('Populated!')
