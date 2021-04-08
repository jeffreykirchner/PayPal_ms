'''
test payments post view
'''
import random
import logging
import json

from rest_framework.renderers import JSONRenderer

from django.test import TestCase

from django.contrib.auth.models import User
from main.views import take_payment_list

class TestPayments(TestCase):
    '''
    test payments post
    '''

    fixtures = ['parameters.json', 'users.json']

    def setUp(self):
        pass

    def test_payments(self):
        '''
        test payments
        '''
        logger = logging.getLogger(__name__)

        user = User.objects.all().first()

        #test double payment
        data = {"items": [{"email": "1234@abc.edu", "amount": 0.01, "note": "hello note", "memo": "hello memo"}], "info": {"payment_id": random.randint(1,9999999),  "email_subject":"email subject"}}
        result = take_payment_list(user, data)
        
        self.assertEqual(201,result['code'])

        result = take_payment_list(user, data)
        self.assertEqual(409,result['code'])

        #test exceeds maximum
        data = {"items": [{"email": str(random.randint(1,99999999)) + "@abc.edu", "amount": 51, "note": "hello note", "memo": "hello memo"}], "info": {"payment_id": random.randint(1,9999999),  "email_subject":"email subject"}}
        result = take_payment_list(user, data)        
        self.assertEqual(201,result['code'])

        result = take_payment_list(user, data)
        self.assertEqual(400,result['code'])
        self.assertEqual('Exceeds max daily earnings',result['text'][0]['detail'])


