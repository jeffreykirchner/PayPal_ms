
from main.models import Payments
from main.serializers import PayementsSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

import logging

class Payment_list_view(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        payments = Payments.objects.all()
        serializer = PayementsSerializer(payments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        logger = logging.getLogger(__name__) 

        logger.info(request.data)

        payments_list = request.data
        return_value_errors = []
        return_value = []

        #check all valid
        for p in payments_list:
            serializer = PayementsSerializer(data=p)

            if not serializer.is_valid():
                return_value_errors.append( {"data": p,
                                             "error": serializer.errors})

        #if any invalid return list
        if len(return_value_errors)>0:
            return Response(return_value_errors, status=status.HTTP_400_BAD_REQUEST)

        #store payments
        for p in payments_list:
            serializer = PayementsSerializer(data=p)

            if serializer.is_valid():
                serializer.save()
                return_value.append(serializer.data)            
        
        return Response(return_value, status=status.HTTP_201_CREATED)