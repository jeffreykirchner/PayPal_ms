
from rest_framework.parsers import JSONParser
from main.models import Payments
from main.serializers import PayementsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'PUT'])
def payment_list_view(request,format=None):

    if request.method == 'GET':
        payment = Payments.objects.all()
        serializer = PayementsSerializer(payment, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PayementsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)