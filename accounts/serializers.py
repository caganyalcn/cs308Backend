from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Hide password from responses

    def create(self, validated_data):
        # Hash password before saving
        validated_data['password'] = validated_data['password']
        return User.objects.create(**validated_data)
