from django.core.cache import cache
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import ReferralCode
from .serializers import ReferralCodeSerializer, UserRegistrationSerializer



class CreateReferralCodeView(generics.GenericAPIView):
    serializer_class = ReferralCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        ReferralCode.objects.filter(user=user).delete()
        expiration_date = timezone.now() + timedelta(days=7)
        referral_code = ReferralCode.objects.create(user=user, expiration_date=expiration_date)
        serializer = self.get_serializer(referral_code)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]