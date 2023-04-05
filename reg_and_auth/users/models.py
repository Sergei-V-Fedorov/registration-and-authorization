from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birthdate = models.DateField()
    city = models.CharField(max_length=36, blank=True)
    telephone = models.CharField(max_length=10, blank=True)

    class Meta:
        permissions = (
            ('can_verify', 'Может верифицировать пользователя'),
        )

    def __str__(self):
        return f"Profile of {self.user}"
