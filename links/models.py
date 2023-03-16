from django.contrib.auth.models import User
from django.db import models

class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    shared_at = models.DateTimeField(auto_now_add=True)

class Follower(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
