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
            raise serializers.ValidationError("이미 사용중인 아이디입니다.")
        return "사용가능한 아이디입니다."

    def validate_email(self, value):
        if Account.objects.filter(email=value).exists():
            raise serializers.ValidationError("해당 이메일은 이미 사용중입니다.")
        return "사용가능한 이메일입니다."

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("패스워드는 최소 %s자 이상이어야 합니다." % 8)
        return value
