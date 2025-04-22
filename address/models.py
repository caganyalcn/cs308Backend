from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.title} - {self.city}"
