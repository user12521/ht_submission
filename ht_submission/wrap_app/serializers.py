from rest_framework import serializers


class SepticSerializer(serializers.Serializer):
    address = serializers.CharField(max_length=300)
    zipcode = serializers.CharField(max_length=5)
    uses_septic = serializers.BooleanField(required=False)
