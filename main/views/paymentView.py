
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from main.models import Payments
from main.serializers import PayementsSerializer

@csrf_exempt
def payment_view(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        payment = Payments.objects.get(pk=pk)
    except Payments.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PayementsSerializer(payment)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PayementsSerializer(payment, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)