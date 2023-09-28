from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone


class CustomUserModel(AbstractUser):
    # applying Custom change to the AbstractUser field.
    profile_avatar = models.ImageField(upload_to='profile_avatar/', blank=True, default='media/default_avatar/author.webp')
    date_joined = models.DateTimeField(default=timezone.now)

    
    def profile_avatar_check(self):
        try:
            return self.profile_avatar.url
        except ValueError:
            return '/media/default_avatar/img_avatar.png'
    # With the @receiver decorator, we can link a signal with a function
    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            CustomUserModel.objects.create(user=instance)
        instance.customusermodel.save()

