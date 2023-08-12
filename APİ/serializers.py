from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product_id", "image"]

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True )  
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=3000, allow_empty_file=False, use_url=True),
        write_only=True
    )

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "permission", "images", "uploaded_images"]

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)

        for image in uploaded_images:
            ProductImage.objects.create(product=product, image=image)

        return product


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

class UpdateCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = updateCode
        fields = '__all__'

class encoder(serializers.ModelSerializer):
    model = CustomUser
    fields = ('password')
    extra_kwargs = {'password': {'write_only': True}}

