from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Dish

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except Exception as e:
            print(f"Error creating user: {e}")  # Log any errors during user creation
            raise serializers.ValidationError("User creation failed")

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'