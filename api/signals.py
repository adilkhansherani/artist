from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Artist

@receiver(post_save, sender=User)
def create_artist_for_user(sender, instance, created, **kwargs):
    if created:
        # Create an associated Artist object for the new user
        Artist.objects.create(user=instance, name=instance.username)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
