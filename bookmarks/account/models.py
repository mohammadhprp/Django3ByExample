from django.db import models
from django.conf import settings

class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  date_of_brith = models.DateTimeField(blank=True, null=True)
  photo = models.ImageField(upload='users/%Y/%m/%d', blank=True)

  def __str__(self):
    return f'Profile for user {self.user.username}'

