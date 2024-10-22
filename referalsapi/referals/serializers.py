from rest_framework import serializers
from .models import ReferralCode, User
from django.utils import timezone

class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ['code', 'expiration_date', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    referral_code = ReferralCodeSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'referral_code']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField( write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'referral_code']

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        user = User.objects.create_user(**validated_data)

        if referral_code:
            try:
                referral = ReferralCode.objects.get(code=referral_code)
                referral.referer = user
                referral.save()
            except ReferralCode.DoesNotExist:
                raise serializers.ValidationError("Error")

        return user
