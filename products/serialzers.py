from rest_framework import serializers
#from django.contrib.auth.models import User
from products.models import Product, User

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User(first_name=validated_data["first_name"],
                    last_name=validated_data["last_name"],
                    username=validated_data["username"],
                    password=validated_data["password"],
                    )
        user.set_password(validated_data["password"])
        user.save()
        return user
    

class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']

    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class ProductModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ['user_id', 'category', 'title', 'description', 'price', 'quantity', 'product_img', 'id']

    def create(self, validated_data):
        print("validated_data", validated_data)
        product = Product.objects.create(**validated_data)
        return product
        