from rest_framework import serializers
from user.models import Account

class AccountSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}

    def validate_username(self, value):
        if Account.objects.filter(username=value).exists():
            return False
        else:
            return True

    def validate_email(self, value):
        if Account.objects.filter(email=value).exists():
            return False
        else:
            return True

    def validate_password(self, value):
        if len(value) < 8:
           return False
        return True

class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('username', 'password')

        def validate_account(self, value):
            pass

