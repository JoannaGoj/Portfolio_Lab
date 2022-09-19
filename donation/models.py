from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=64)


TYPE_CHOICES = (
    (1, "Foundation"),
    (2, "Local Foundraiser"),
    (3, "NGO")

)


class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=150)
    type = models.IntegerField(choices=TYPE_CHOICES)
    categories = models.ManyToManyField('Category')


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField('Category')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    address = models.CharField(max_length=180)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=64)
    zip_code = models.IntegerField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)