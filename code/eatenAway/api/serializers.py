from rest_framework import serializers
from user.models import Account
from food.models import Food, FoodComment


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = ('menuname', 'category', 'country', 'taste', 'stock', 'description')


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('username', 'password')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodComment
        fields = '__all__'


class AccountProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('area', 'sex', 'comment')