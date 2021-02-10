'''
get payments across a date range
'''
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from main.models import Payments
from main.serializers import PayementsSerializer
from main.globals import get_whitelist_ip

class Payment_range_view(APIView):
    '''
    Payments within a date range
    '''
    #get the payments from the specified date ranage.
    def get(self, request, start_date,end_date):
        '''
        Get payments within the specified date range
        '''
        logger = logging.getLogger(__name__)

        logger.info(f"Get payments between: {start_date} and {end_date}")

        #check ip on white list
        ip_whitelist = get_whitelist_ip(request)
        if not ip_whitelist:
            logger.info('Get payments list IP Not Found')
            return Response({"detail": "Invalid IP Address"}, status=status.HTTP_401_UNAUTHORIZED)

        logger.info('Get payments list: {ip_whitelist}')

        payments = Payments.objects.all()
        serializer = PayementsSerializer(payments, many=True)

        return Response(serializer.data)