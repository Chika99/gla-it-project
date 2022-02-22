from datetime import datetime

from app.models import Order, Tag, OrderImage, Message, Bid, User


class OrderDto:
    id: int
    user: User
    title: str
    description: str
    start_price: int
    highest_price: int
    publish_time: datetime
    end_time: datetime
    status: str
    tags: list[Tag]
    images: list[OrderImage]

    def __init__(self, order: Order):
        for k in order.__dict__.keys():
            setattr(self, k, order.__dict__.get(k))
        self.user = order.user
        self.tags = [tag for tag in Tag.objects.filter(orders__id=order.id)]
        self.images = [img for img in OrderImage.objects.filter(order__id=order.id)]
        b = Bid.objects.filter(order__id=order.id).order_by('-price').first()
        self.highest_price = b.price if b else None


class MessageDto:
    id: int
    username: str
    content: str
    time: datetime
    reply_id: int

    def __init__(self, message: Message):
        for k in message.__dict__.keys():
            setattr(self, k, message.__dict__.get(k))
        self.username = message.user.username
        self.reply_id = message.reply.id if message.reply else None


class BidDto:
    id: int
    username: str
    price: int
    time: datetime

    def __init__(self, bid: Bid):
        for k in bid.__dict__.keys():
            setattr(self, k, bid.__dict__.get(k))
        self.username = bid.user.username


class OrderDetailDto(OrderDto):
    messages: list[MessageDto]
    bids: list[BidDto]

    def __init__(self, order: Order):
        super().__init__(order)
        self.messages = [MessageDto(message) for message in Message.objects.filter(order__id=order.id)]
        self.bids = [BidDto(bid) for bid in Bid.objects.filter(order__id=order.id).order_by('-id')]


class UserDetailDto:
    id: int
    username: str
    avatar: str
    tel: int
    balance: int
    credit_level: int
    address: int
    orders: list[OrderDto]

    def __init__(self, user: User):
        for k in user.__dict__.keys():
            setattr(self, k, user.__dict__.get(k))
        self.avatar = user.avatar.url if user.avatar else None
        self.orders = [OrderDto(order) for order in Order.objects.filter(user__id=user.id)]
