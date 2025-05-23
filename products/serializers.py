from rest_framework import serializers
from .models import Product, Category, Favorite

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'serial_number', 'description', 'price', 
                 'stock_quantity', 'category_id', 'category_name', 'warranty_status', 
                 'distributor_info', 'image_url', 'avg_rating', 'rating_count', 
                 'created_at', 'updated_at']

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'product', 'product_id', 'created_at']
        read_only_fields = ['id', 'product', 'created_at']
