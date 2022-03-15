from datetime import datetime

from app.models import Order, Tag, OrderImage, Message, Bid, User, Comment


class OrderDto:
    id: int
    seller: User
    bid: Bid
    buyer: User
    title: str
    description: str
    start_price: float
    highest_price: float
    publish_time: datetime
    end_time: datetime
    status: str
    tags: list[Tag]
    images: list[OrderImage]

    def __init__(self, order: Order, bid=None):
        for k in order.__dict__.keys():
            setattr(self, k, order.__dict__.get(k))
        self.start_price = round(self.start_price / 100, 2)
        self.seller = order.seller
        if self.status == 'F':
            self.buyer = order.buyer
        self.bid = bid
        self.tags = [tag for tag in Tag.objects.filter(orders__id=order.id)]
        self.images = [img for img in OrderImage.objects.filter(order__id=order.id)]
        b = Bid.objects.filter(order__id=order.id).order_by('-price').first()
        self.highest_price = b.price if b else None
        if self.highest_price:
            self.highest_price = round(self.highest_price / 100, 2)


class OrderDetailDto(OrderDto):
    messages: list[Message]
    bids: list[Bid]
    comments: list[Comment]

    def __init__(self, order: Order):
        super().__init__(order)
        self.messages = [message for message in Message.objects.filter(order__id=order.id)]
        self.bids = [bid for bid in Bid.objects.filter(order__id=order.id).order_by('-id')]
        self.comments = [comment for comment in Comment.objects.filter(order__id=order.id)]


class UserDetailDto:
    id: int
    username: str
    avatar: str
    tel: int
    balance: float
    credit_level: int
    address: str
    orders: list[OrderDto]

    def __init__(self, user: User):
        for k in user.__dict__.keys():
            setattr(self, k, user.__dict__.get(k))
        self.balance = round(self.balance / 100, 2)
        self.avatar = user.avatar.url if user.avatar else None
        # 添加自己的订单
        self.orders = [OrderDto(order) for order in Order.objects.filter(seller_id=user.id)]
        # 添加自己下注的
        self.orders.extend([
            OrderDto(order, bid=Bid.objects.filter(order__id=order.id, user__id=user.id).order_by('-price').first())
            for order in Order.objects.filter(bid__user_id=user.id).distinct()
        ])
        # 按照时间排序
        self.orders = sorted(self.orders, key=lambda x: x.bid.time if x.bid else x.publish_time, reverse=True)
