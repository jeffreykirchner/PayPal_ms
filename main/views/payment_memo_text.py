'''
get payments with search_text in memo
'''

import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from main.models import Payments
from main.serializers import PayementsSerializer

class PaymentMemoText(APIView):
    '''
    Return payments with text in memo
    '''
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, search_text):
        '''
        Get payments with spcified text in memo
        '''
        logger = logging.getLogger(__name__)

        logger.info(f"Get payments with text: {search_text}, user: {request.user}")

        payments = Payments.objects.filter(memo__contains = search_text)

        serializer = PayementsSerializer(payments, many=True)

        return Response(serializer.data)