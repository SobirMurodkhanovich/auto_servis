from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('employee', 'EMPLOYEE'),
        ('user', 'USER'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

    def __str__(self):
        return self.username


class AutoMobile(models.Model):
    customer_name = models.CharField(max_length=25)
    customer_phone_number = models.CharField(max_length=25)
    automobile_number = models.CharField(max_length=10)
    mileage = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} {self.automobile_number} {self.created_at}"


class Service(models.Model):
    service_name = models.CharField(max_length=25)
    service_price = models.IntegerField()

    def __str__(self):
        return f"{self.service_name} {self.service_price}"


class AutoService(models.Model):
    automobile = models.ForeignKey(AutoMobile, on_delete=models.SET_NULL, null=True)
    services = models.ManyToManyField(Service)
    total_sum = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.automobile} - {self.created_at}"
