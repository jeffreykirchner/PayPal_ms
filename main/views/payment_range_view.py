'''
get payments across a date range
'''
from datetime import datetime

import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from main.models import Payments
from main.serializers import PayementsSerializer
from main.globals import make_tz_aware_utc

class PaymentRangeView(APIView):
    '''
    Payments within a date range
    '''
    permission_classes = [permissions.IsAuthenticated]

    #get the payments from the specified date ranage.
    def get(self, request, start_date, end_date, source_time_zone):
        '''
        Get payments within the specified date range
        '''
        logger = logging.getLogger(__name__)

        logger.info(f"Get payments between: {start_date} and {end_date}")

        try:
            d_start_date = datetime.strptime(start_date,"%Y-%m-%d")
            d_end_date = datetime.strptime(end_date,"%Y-%m-%d")

            d_start_date = make_tz_aware_utc(d_start_date, 0, 0, 0, source_time_zone)
            d_end_date = make_tz_aware_utc(d_end_date, 23, 59, 59, source_time_zone)

        except Exception  as exce:
            return Response({"detail": f"Invalid Dates: {start_date} {end_date}, Format: YYYY-MM-DD"},
                             status=status.HTTP_400_BAD_REQUEST)

        #check ip on white list
        #ip_whitelist = get_whitelist_ip(request)
        # if not ip_whitelist:
        #     logger.info('Get payments list IP Not Found')
        #     return Response({"detail": "Invalid IP Address"}, status=status.HTTP_401_UNAUTHORIZED)

        logger.info(f'Get payments list: {request.user}')

        payments = Payments.objects.filter(timestamp__gte = d_start_date)\
                                   .filter(timestamp__lte = d_end_date)

        serializer = PayementsSerializer(payments, many=True)

        return Response(serializer.data)