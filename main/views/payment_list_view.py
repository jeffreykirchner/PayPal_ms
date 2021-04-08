'''
View for taking and returning a list of all payments
'''
from datetime import datetime, timedelta
import logging
import pytz

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from django.db.models import  Sum

from main.models import Payments, Parameters
from main.serializers import PayementsSerializer
from main.globals import paypal_action

class PaymentListView(APIView):
    '''
    return a list of all payments or take a list for payment
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        '''
        Get all payments in list format
        '''
        logger = logging.getLogger(__name__)

        logger.info(f'Get payments list: {request.user}')

        #get paypal balance
        #data = {}
        # data["sender_batch_header"] = {"sender_batch_id" : f'{user}_{payments_info["payment_id"]}',
        #                                "email_subject" : payments_info["email_subject"]}
        # data["items"] = items

        # logger.info(f'Payment list post data: {data}')

        #val = paypal_action('v2/wallet/balance-accounts', "get", data)

        #logger.info(val)

        payments = Payments.objects.all()
        serializer = PayementsSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request):
        '''
        handle /payments post
        '''
        logger = logging.getLogger(__name__)
        logger.info(request.data)

        result = take_payment_list(request.user, request.data)

        return Response(result['text'], status=result['code'])

def take_payment_list(user, data):
    '''
    Add new payments from a list
    {"items": [{"email": "1234@abc.edu", "amount": 3, "note": "hello note", "memo": "hello memo"}], "info": {"payment_id": "1",  "email_subject":"email subject"}}
    '''

    params = Parameters.objects.first()

    logger = logging.getLogger(__name__)

    payments_list = data["items"]
    payments_info = data["info"]

    logger.info(f'Store payments list: {user}')

    #check payments do not exceed max amount per 24 hour period
    return_value_errors = []
    return_value = []

    logger.info(f'Payments List: {payments_list}')

    #check all valid
    items=[]
    counter = 1
    for payment in payments_list:
        serializer = PayementsSerializer(data=payment)

        if not serializer.is_valid():
            return_value_errors.append( {"data": payment,
                                         "detail": serializer.errors})
        else:
            amount = float(serializer.data["amount"])
            max_daily_earnings = params.max_daily_earnings
            email = serializer.data["email"].strip().lower()

            d_minus24 = datetime.now(pytz.UTC) - timedelta(hours=24)

            earnings_last24 = Payments.objects.filter(timestamp__gte=d_minus24) \
                                                .filter(email = email)\
                                                .aggregate(Sum('amount'))

            logger.info(f"Earnings last 24 hours {email}, {earnings_last24}")

            if earnings_last24['amount__sum']:
                earnings_total = amount + float(earnings_last24['amount__sum'])
            else:
                earnings_total = amount

            if earnings_total > max_daily_earnings :
                return_value_errors.append( {"data": payment,
                                             "detail": "Exceeds max daily earnings"})
            else:
                #paypal items
                items.append({"amount": {
                                    "value": serializer.data["amount"],
                                    "currency": "USD"
                                },
                            "recipient_type": "EMAIL",
                            "note": serializer.data["note"],
                            "sender_item_id": f'{payments_info["payment_id"]}_{counter}',
                            "receiver": serializer.data["email"]
                        })

                counter += 1

    #if any invalid return list
    if len(return_value_errors)>0:
        return {'text' : return_value_errors,
                'code' : status.HTTP_400_BAD_REQUEST}

    #send payments to paypal
    data = {}
    data["sender_batch_header"] = {"sender_batch_id" : f'{user}_{payments_info["payment_id"]}',
                                   "email_subject" : payments_info["email_subject"]}
    data["items"] = items

    logger.info(f'Payment list post data: {data}')

    val = paypal_action('v1/payments/payouts', "post", data)

    #check for duplicate payment
    if val.get("name","not found") == "USER_BUSINESS_ERROR":

        logger.info('PayPal Double Payment')
        return {'text' : {"detail": "PayPal Double Payment"},
                'code' : status.HTTP_409_CONFLICT}
        
    #store payments
    for payment in payments_list:
        serializer = PayementsSerializer(data=payment)

        if serializer.is_valid():
            serializer.validated_data["email"] = serializer.validated_data["email"].strip().lower()
            serializer.validated_data["app"] = user
            serializer.validated_data["payout_batch_id_local"] = payments_info["payment_id"]
            serializer.validated_data["payout_batch_id_paypal"] = val["batch_header"]["payout_batch_id"]

            serializer.save()
            return_value.append(serializer.data)

    return {'text' : return_value, 'code' : status.HTTP_201_CREATED}


