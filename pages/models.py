from django.db import models

# Create your models here.
class auth(models.Model):
    full_name = models.CharField(max_length=40, blank=False)
    phone_number = models.BigIntegerField(blank=False)
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=40, blank=False)