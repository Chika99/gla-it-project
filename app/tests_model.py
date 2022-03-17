# from anyio import BusyResourceError
import datetime
from django.test import TestCase

from app.models import Order, User


class UserTest(TestCase):

    #create default database for test
    def setUp(self) -> None:
        User.objects.create(username="test0", tel=654321, balance=0, credit_level=10, address="Glasgow")

    #test for create a user and find this user in database
    def test1_CreateUser(self):
        User.objects.create(username="test1", tel=123456, balance=100, credit_level=0, address="London")
        a = User.objects.get(username="test1")
        self.assertEqual(a.username, "test1")
        self.assertEqual(a.tel, 123456)
        self.assertEqual(a.balance, 100)
        self.assertEqual(a.credit_level, 0)
        self.assertEqual(a.address, "London")

    #test for delete the default user which is created in setUp()
    def test2_DeleteUser(self):
        a = User.objects.get(username="test0")
        a.delete()
        b = User.objects.filter(username="test0")
        c = len(b)
        self.assertEqual(c, 0)

    #test for update a user and find this user in database
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

    #test for find user
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

class OrderTest(TestCase):

    #create default datebase for test
    def setUp(self) -> None:
        seller0 = User.objects.create(username="seller0")
        buyer0 = User.objects.create(username="buyer0")
        Order.objects.create(id=0, seller=seller0, buyer=buyer0, title="test0", description="new", start_price=200, end_time=datetime.datetime(2022, 3, 21, 0, 0))

    #test for create an order and find it
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

    #test for delete an order
    def test6_DeleteOrder(self):
        a = Order.objects.get(id=0)
        a.delete()
        b = Order.objects.filter(id=0)
        c = len(b)
        self.assertEqual(c, 0)

    #test for update an order and check its information correct or not   
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

    #test for find order
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



    