from datetime import datetime

from app.models import Order, Tag, OrderImage, Message, Bid


class OrderDto:
    id: int
    username: str
    title: str
    description: str
    start_price: int
    highest_price: int
    publish_time: datetime
    end_time: datetime
    status: str
    tags: list[str]
    images: list[str]

    def __init__(self, order: Order):
        for k in order.__dict__.keys():
            setattr(self, k, order.__dict__.get(k))
        self.username = order.user.username
        self.tags = [tag.name for tag in Tag.objects.filter(orders__id=order.id)]
        self.images = [img.img.url for img in OrderImage.objects.filter(order__id=order.id)]
        b = Bid.objects.filter(order__id=order.id).order_by('price').reverse().first()
        self.highest_price = b.price if b else 0


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
