from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    pass

class ReferralCode(models.Model):
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referal_code')
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    referer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referals', null=True, blank=True)

