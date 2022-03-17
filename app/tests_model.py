# from anyio import BusyResourceError
import datetime
from django.test import TestCase

from app.models import Bid, Order, Tag, User

#test for models.User
class UserTest(TestCase):

    #create default database for test
    def setUp(self) -> None:
        User.objects.create(username="test0", tel=654321, balance=0, credit_level=10, address="Glasgow")

    #test for creating a user and find this user in database
    def test1_CreateUser(self):
        User.objects.create(username="test1", tel=123456, balance=100, credit_level=0, address="London")
        a = User.objects.get(username="test1")
        self.assertEqual(a.username, "test1")
        self.assertEqual(a.tel, 123456)
        self.assertEqual(a.balance, 100)
        self.assertEqual(a.credit_level, 0)
        self.assertEqual(a.address, "London")

    #test for deleting the default user which is created in setUp()
    def test2_DeleteUser(self):
        a = User.objects.get(username="test0")
        a.delete()
        b = User.objects.filter(username="test0")
        c = len(b)
        self.assertEqual(c, 0)

    #test for updating a user and find this user in database
    def test3_UpdateUser(self):
        a = User.objects.get(username="test0")
        a.username = "update"
        a.tel = 100
        a.balance = 1
        a.credit_level = 100
        a.address = "West"
        a.save()
        b = User.objects.get(username="update")
        self.assertEqual(b.username, "update")
        self.assertEqual(b.tel, 100)
        self.assertEqual(b.balance, 1)
        self.assertEqual(b.credit_level, 100)
        self.assertEqual(b.address, "West")

    #test for finding user
    def test4_FindUser(self):
        User.objects.create(username="test1", tel=123456, balance=100, credit_level=0, address="London")
        a = User.objects.filter(username__contains="test")
        #can find two objects
        self.assertEqual(len(a), 2)
        b = User.objects.filter(tel__contains=123)
        #can find one obejct
        self.assertEqual(len(b), 1)
        c = User.objects.filter(balance__contains=999)
        #none can be found
        self.assertEqual(len(c), 0)

#test for models.Order
class OrderTest(TestCase):

    #create default datebase for test
    def setUp(self) -> None:
        seller0 = User.objects.create(username="seller0")
        buyer0 = User.objects.create(username="buyer0")
        Order.objects.create(id=0, seller=seller0, buyer=buyer0, title="test0", description="new", start_price=200, end_time=datetime.datetime(2022, 3, 21, 0, 0))

    #test for creating an order and find it
    def test5_CreateOrder(self):
        seller1 = User.objects.create(username="seller1")
        buyer1 = User.objects.create(username="buyer1")
        Order.objects.create(id=1, seller=seller1, buyer=buyer1, title="test", description="null", start_price=100, end_time=datetime.datetime(2022, 3, 20, 0, 0))
        a = Order.objects.get(title="test")
        self.assertEqual(a.title, "test")
        self.assertEqual(a.buyer, buyer1)
        self.assertEqual(a.seller, seller1)
        self.assertEqual(a.description, "null")
        self.assertEqual(a.end_time, datetime.datetime(2022, 3, 20, 0, 0))

    #test for deleting an order
    def test6_DeleteOrder(self):
        a = Order.objects.get(id=0)
        a.delete()
        b = Order.objects.filter(id=0)
        c = len(b)
        self.assertEqual(c, 0)

    #test for updating an order and check its information correct or not   
    def test7_UpdateOrder(self):
        seller1 = User.objects.create(username="seller1")
        buyer1 = User.objects.create(username="buyer1")
        a = Order.objects.get(id=0)
        a.seller=seller1
        a.buyer=buyer1
        a.title = "apple"
        a.description = "fresh"
        a.start_price = 5
        a.end_time=datetime.datetime(2023, 3, 20, 0, 0)
        a.save()
        b = Order.objects.get(id=0)
        self.assertEqual(b.seller, seller1)
        self.assertEqual(b.buyer, buyer1)
        self.assertEqual(b.title, "apple")
        self.assertEqual(b.start_price, 5)
        self.assertEqual(b.description, "fresh")
        self.assertEqual(b.end_time, datetime.datetime(2023, 3, 20, 0, 0))

    #test for finding order
    def test8_FindOrder(self):
        seller1 = User.objects.create(username="seller1")
        buyer1 = User.objects.create(username="buyer1")
        Order.objects.create(id=1, seller=seller1, buyer=buyer1, title="test", description="null", start_price=100, end_time=datetime.datetime(2022, 3, 20, 0, 0))
        
        a = Order.objects.filter(title__contains="te")
        #can find two objects
        self.assertEqual(len(a), 2)
        b = Order.objects.filter(start_price__contains=100)
        #can find one obejct
        self.assertEqual(len(b), 1)
        c = Order.objects.filter(description__contains="pineapple")
        #none can be found
        self.assertEqual(len(c), 0)

#test for models.Tag
class TagTest(TestCase):

    #set up default database for test
    def setUp(self):
        Tag.objects.create(id=0, name="test0")
    
    #test for creating Tag
    def test9_CreateTag(self):
        Tag.objects.create(id=1, name="tag1")
        a = Tag.objects.get(id=1)
        self.assertEqual(a.id, 1)
        self.assertEqual(a.name,"tag1")

    #test for deleting Tag
    def test10_DeleteTag(self):
        a = Tag.objects.get(id=0)
        a.delete()
        b = Tag.objects.filter(id=0)
        c = len(b)
        self.assertEqual(c, 0)

    #test for updating Tag
    def test11_UpdateTag(self):
        a = Tag.objects.get(id=0)
        a.id = 3
        a.name = "update"
        a.save()
        b = Tag.objects.get(id=3)
        self.assertEqual(a.id, 3)
        self.assertEqual(a.name,"update")

    #test for finding Tag
    def test12_FindTag(self):
        Tag.objects.create(id=1, name="tag1")
        a = Tag.objects.filter(name__contains="t")
        self.assertEqual(len(a), 2)
        b = Tag.objects.filter(id__contains=123)
        self.assertEqual(len(b), 0)

#test for models.Bid
class BidTest(TestCase):

    #create default database for testing
    def setUp(self):
        seller0 = User.objects.create(username="seller0")
        buyer0 = User.objects.create(username="buyer0")
        Order0 = Order.objects.create(id=0, seller=seller0, buyer=buyer0, title="test0", description="new", start_price=200, end_time=datetime.datetime(2022, 3, 21, 0, 0))    
        Bid.objects.create(id=0, order=Order0, user=buyer0, price=300)
    
    #test for creating bid
    def test13_CreateBid(self):
        seller1 = User.objects.create(username="seller1")
        buyer1 = User.objects.create(username="buyer1")
        Order1 = Order.objects.create(id=1, seller=seller1, buyer=buyer1, title="test1", description="old", start_price=100, end_time=datetime.datetime(2023, 3, 21, 0, 0))    
        Bid.objects.create(id=1, order=Order1, user=buyer1, price=500)
        a = Bid.objects.get(id=1)
        self.assertEqual(a.id, 1)
        self.assertEqual(a.order, Order1)
        self.assertEqual(a.user, buyer1)
        self.assertEqual(a.price, 500)

    #test for deleting bid
    def test14_DeleteBid(self):
        a = Bid.objects.get(id=0)
        a.delete()
        b = Bid.objects.filter(id=0)
        self.assertEqual(len(b), 0)

    #test for updating bid
    def test15_UpdateBid(self):
        #create some argument for setting to current bid 
        seller1 = User.objects.create(username="seller1")
        buyer1 = User.objects.create(username="buyer1")
        Order1 = Order.objects.create(id=1, seller=seller1, buyer=buyer1, title="test1", description="old", start_price=100, end_time=datetime.datetime(2023, 3, 21, 0, 0))    
        # get bid whose id is 0
        a = Bid.objects.get(id=0)
        a.id = 3
        a.order = Order1
        a.user = seller1
        a.price = 1000
        a.save()
        self.assertEqual(a.id, 3)
        self.assertEqual(a.order, Order1)
        self.assertEqual(a.user, seller1)
        self.assertEqual(a.price, 1000)

    #test for finding bid
    def test16_FindBid(self):
        #create an new bid
        seller1 = User.objects.create(username="seller1")
        buyer1 = User.objects.create(username="buyer1")
        Order1 = Order.objects.create(id=1, seller=seller1, buyer=buyer1, title="test1", description="old", start_price=100, end_time=datetime.datetime(2023, 3, 21, 0, 0))    
        Bid.objects.create(id=1, order=Order1, user=buyer1, price=500)
        #there are 2 bids in database now
        a = Bid.objects.filter(price__contains=0)
        self.assertEqual(len(a), 2)
        b = Bid.objects.filter(price__contains=500)
        self.assertEqual(len(b), 1)
        c = Bid.objects.filter(user=buyer1)
        self.assertEqual(len(c), 1)



