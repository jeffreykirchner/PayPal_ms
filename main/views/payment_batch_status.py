'''
return paypal batch payment status
'''

import logging
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.core.serializers.json import DjangoJSONEncoder

from main.globals import paypal_action

class PaymentBatchStatus(APIView):
    '''
    Return paypal batch payment status
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, batch_id):
        '''
        Get payments with spcified text in memo
        '''
        logger = logging.getLogger(__name__)

        logger.info(f"Get batch payment status: batch id:{batch_id}, user: {request.user}")

        val = paypal_action(f'v1/payments/payouts/{batch_id}', "get", {})

        return Response(val, status.HTTP_200_OK)