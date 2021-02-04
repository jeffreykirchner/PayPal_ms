from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from main.models import Payments
from main.serializers import PayementsSerializer

@csrf_exempt
def payment_list_view(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        payment = Payments.objects.all()
        serializer = PayementsSerializer(payment, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PayementsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)