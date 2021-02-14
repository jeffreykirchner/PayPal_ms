'''
 PayPal API functions
'''
import logging

import requests
import json

from django.conf import settings

from main.models import Parameters

def paypal_auth():
    '''
    check if paypal needs a new token
    '''
    logger = logging.getLogger(__name__)
    logger.info("paypal_auth")

    prm = Parameters.objects.first()

    headers = {"Accept": "application/json",
               "Accept-Language": "en_US"}

    data = {"grant_type":"client_credentials"}

    req = requests.post(f'{settings.PAYPAL_URL}/v1/oauth2/token',
                       headers = headers,
                       data = data,
                       auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET))

    req_json = req.json()
    #logger.info(req_json)

    logger.info(f'paypal_auth status code: {req.status_code}')

    if req.status_code == 200:
        prm.paypal_token = req_json["access_token"]
        prm.save()

        return True
    
    return False

def paypal_action(val, mode, data):
    '''
    check if paypal token needs refresh
    val: https://api-m.sandbox.paypal.com/v2/{val}
    '''
    logger = logging.getLogger(__name__)
    logger.info(f"paypal_action {val}")

    prm = Parameters.objects.first()

    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {prm.paypal_token}"}

    if mode == "get":
        req = requests.get(f'{settings.PAYPAL_URL}/{val}',
                           headers = headers)
    else:
        logger.info("post")
        req = requests.post(f'{settings.PAYPAL_URL}/{val}',
                            headers = headers,
                            json = data)
    
    #check failed auth code
    if req.status_code == 401:
        if paypal_auth():
            return paypal_action(val, mode, data)
             
        logger.info('paypal_action: Authorization failed')
        return {'error':'Authorization failed'}
    
    req_json = req.json()
    logger.info(f'paypal_action {req_json}')

    return req_json
        



