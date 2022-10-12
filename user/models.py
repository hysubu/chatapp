from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class UserMsg(models.Model):
    message = models.JSONField()
    sender = models.CharField(max_length=100)
    reciver = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


