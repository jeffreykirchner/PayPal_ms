from rest_framework import serializers
from main.models import Payments

class PayementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['id', 'email', 'amount', 'memo']

# class PayementsSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
    
#     email = serializers.EmailField(max_length = 250)
#     amount = serializers.DecimalField(min=0)
#     memo = serializers.CharField(max_length = 250) 
    

#     def create(self, validated_data):
#         """
#         Create and return a new 'Payements' instance, given the validated data.
#         """
#         return Payments.objects.create(**validated_data)

