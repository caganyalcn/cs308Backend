from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'model',
            'description',
            'price',
            'stock_quantity',
            'category',
            'warranty_status',
            'distributor_info',
            'serial_number',
            'image_url',
            'discount_rate',
            'cost_price',
            'avg_rating',
            'rating_count',
            'is_priced',
        ]
