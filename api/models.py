from django.db import models
from django.contrib.auth.models import User

class Artist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class Work(models.Model):
    link = models.CharField(max_length=255)
    work_type = models.CharField(
        max_length=10,
        choices=[('YT', 'Youtube'), ('IG', 'Instagram'), ('Other', 'Other')]
    )
    artist = models.ManyToManyField(Artist, related_name='artists')