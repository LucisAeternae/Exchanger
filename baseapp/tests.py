from django.test import TestCase, Client
from django.shortcuts import reverse
from baseapp.models import Offer, Profile, CustomUser, Game, Category
from baseapp.views import transaction
from djmoney.money import Money
from django.contrib.auth.hashers import make_password

class TestAccountTransaction(TestCase):
    def setUp(self):
        self.user1 = CustomUser(username='firstuser',
                        password=make_password('firstuser'),
                        email='firstuser@gmail.com')
        self.user1.save()
        self.game1 = Game(name='game1')
        self.game1.save()
        self.category1 = Category(game=self.game1, title='category1')
        self.category1.save()
        self.profile1 = Profile(user=self.user1, username=self.user1.username,
                        money=Money(0.00, 'USD'))
        self.profile1.save()
        self.offer1 = Offer(user=self.user1, title='offer1',
                        category=self.category1, price=Money(50.00, 'USD'))
        self.offer1.save()
        self.offer2 = Offer(user=self.user1,title='offer2',
                        category=self.category1, price=Money(200.00, 'USD'))
        self.offer2.save()
        self.user2 = CustomUser(username='seconduser',
                        password=make_password('seconduser'),
                        email='seconduser@gmail.com')
        self.user2.save()
        self.profile2 = Profile(user=self.user2, username=self.user2.username,
                         money=Money(100.00, 'USD'))
        self.profile2.save()
        client = Client()

    def test_login(self):
        response = self.client.post('/signin/', {'username': 'firstuser',
                        'password': 'firstuser'})
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'firstuser')

    def test_transation_succed(self):
        print('before purchase', self.offer1.price, self.profile1.money, self.profile2.money)
        response = self.client.post('/signin/', {'username': 'seconduser',
                        'password': 'seconduser'})
        response = self.client.get('/offer/1/purchase/')
        response = self
        print('after purchase', self.offer1.price, self.profile1.money, self.profile2.money)
        self.assertEqual(self.profile1.money, Money(50, 'USD'))

    def test_transation_faild_not_enough(self):
        response = self.client.post('/signin/', {'username': 'seconduser',
                        'password': 'seconduser'})
        response = self.client.get('/offer/2/purchase/')
        response = self.client.get('/offer/2/')
        self.assertContains(response, 'Not enough money!')

    def test_transation_selfbuy_faild(self):
        response = self.client.post('/signin/', {'username': 'firstuser',
                        'password': 'firstuser'})
        response = self.client.get('/offer/2/purchase/')
        response = self.client.get('/offer/2/')
        self.assertContains(response, 'You cannot buy from yourself!')
