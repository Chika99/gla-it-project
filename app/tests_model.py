from django.test import TestCase

from app.models import User


class DjangoTest(TestCase):

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




    