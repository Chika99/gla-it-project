import datetime
from django.test import SimpleTestCase

from app.forms import BidForm, CommentForm, MessageForm, OrderForm, RegisterForm, UserModifyForm

#test for RegisterForm
class TestRegisterForms(SimpleTestCase):
    
    #can the form be generated normally if there is data passed in
    def test1_RegisterFormValid(self):
        form  = RegisterForm(data={
            'password': '123abc',
            'tel': '123456',
            'balance': '100.1',
            'credit_level': '10',
            'address': 'glasgow'
        })
        self.assertTrue(form.is_valid)

    #will the form report an error when no data is passed in?
    def test2_RegisterFormNull(self):
        form = RegisterForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

#test for OrderForm
class TestOrderForm(SimpleTestCase):

    #test for successfully generating the OrderForm
    def test3_OrderFormValid(self):
        form = OrderForm(data={
            'end_time': datetime.datetime(2023, 3, 21, 0, 0),
            'start_price': '100.1'
        })
        self.assertTrue(form.is_valid)

    #test for unsuccessfully generating the OrderForm
    def test4_OrderFormNull(self):
        form = OrderForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)  

#test for BidForm
class TestBidForm(SimpleTestCase):

    def test5_BidFormValid(self):
        form = BidForm(data={
            'price': '100.1'
        })
        self.assertTrue(form.is_valid)

    def test6_BidFormNull(self):
        form = BidForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)  

#test for MessageForm
class TestMessageForm(SimpleTestCase):

    def test7_MessageFormValid(self):
        form = MessageForm(data={})
        self.assertTrue(form.is_valid)

    def test8_MessageFormNull(self):
        form = MessageForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)  

#test for CommentForm
class TestCommentForm(SimpleTestCase):

    def test9_CommentFormValid(self):
        form = CommentForm(data={})
        self.assertTrue(form.is_valid)

    def test10_CommentFromNull(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

#test for UserModifyForm
class TestUserModifyForm(SimpleTestCase):

    def test11_UserModifyFormValid(self):
        form = UserModifyForm(data={})
        self.assertTrue(form.is_valid) 
    
    def test12_UserModifyFromNull(self):
        form = UserModifyForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
