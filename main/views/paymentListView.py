
from main.models import Ip_whitelist,Payments,Parameters
from main.serializers import PayementsSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from datetime import datetime, timedelta,timezone
from django.db.models import Avg, Count, Min, Sum

import logging
import pytz

class Payment_list_view(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        logger = logging.getLogger(__name__) 

        remote_ip = request.META["REMOTE_ADDR"]
        logger.info(f'Get payments list: {remote_ip}')

        #check for IP on white list
        if not Ip_whitelist.objects.filter(ip_address=remote_ip).exists():
            return Response("Invalid IP Address", status=status.HTTP_401_UNAUTHORIZED)
        
        payments = Payments.objects.all()
        serializer = PayementsSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        params = Parameters.objects.first()
        
        logger = logging.getLogger(__name__) 
        logger.info(request.data)

        remote_ip = request.META["REMOTE_ADDR"]
        logger.info(f'Get payments list: {remote_ip}')

        #check for IP on white list
        if not Ip_whitelist.objects.filter(ip_address=remote_ip).exists():
            return Response("Invalid IP Address", status=status.HTTP_401_UNAUTHORIZED)

        #check payments do not exceed max amount per 24 hour period
        
        payments_list = request.data
        return_value_errors = []
        return_value = []

        #check all valid
        for p in payments_list:
            serializer = PayementsSerializer(data=p)

            if not serializer.is_valid():
                return_value_errors.append( {"data": p,
                                             "error": serializer.errors})
            else:
                amount = float(serializer.data["amount"])
                max_daily_earnings = params.max_daily_earnings
                email = serializer.data["email"].strip().lower()

                d_minus24 = datetime.now(pytz.UTC) - timedelta(hours=24)

                earnings_last24 = Payments.objects.filter(timestamp__gte=d_minus24) \
                                                  .filter(email = email)\
                                                  .aggregate(Sum('amount')) 

                logger.info(f"Earnings last 24 hours {email}, {earnings_last24}")

                earnings_total = amount + float(earnings_last24['amount__sum'])

                if earnings_total > max_daily_earnings :
                     return_value_errors.append( {"data": p,
                                                  "error": "Exceeds max daily earnings"})

        #if any invalid return list
        if len(return_value_errors)>0:
            return Response(return_value_errors, status=status.HTTP_400_BAD_REQUEST)

        #store payments
        for p in payments_list:
            serializer = PayementsSerializer(data=p)

            if serializer.is_valid():
                serializer.validated_data["email"] = serializer.validated_data["email"].strip().lower()
                serializer.save()
                return_value.append(serializer.data)            
        
        return Response(return_value, status=status.HTTP_201_CREATED)