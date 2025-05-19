from rest_framework import serializers

class PriceSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)

class DiscountSerializer(serializers.Serializer):
    product_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), min_length=1)
    percent = serializers.IntegerField(min_value=1, max_value=90)
