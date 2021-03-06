from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='photo/%Y%m%d/',blank=True)
    description = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)
