from rest_framework import serializers
from main.models import Payments

# class PayementsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payments
#         fields = ['id', 'email', 'amount', 'memo','timestamp']

class PayementsSerializer(serializers.Serializer):
    '''
    serialize REST version of payment model
    '''
    id = serializers.IntegerField(read_only=True)
    
    email = serializers.EmailField(max_length = 250)
    amount = serializers.DecimalField(max_digits=5,decimal_places=2)
    memo = serializers.CharField(max_length = 250) 
    timestamp = serializers.DateTimeField(format="%m/%d/%Y %H:%M:%S %Z",required=False)
    ip_whitelist = serializers.IPAddressField(required=False)
    note = serializers.CharField(max_length = 250)

    def create(self, validated_data):
        """
        Create and return a new 'Payements' instance, given the validated data.
        """
        return Payments.objects.create(**validated_data)

