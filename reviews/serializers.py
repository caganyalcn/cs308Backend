from rest_framework import serializers
from .models import Review
from accounts.serializers import UserSerializer
from products.serializers import ProductSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'approved', 'created_at']
        read_only_fields = ['approved', 'created_at'] 