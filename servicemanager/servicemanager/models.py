from django.db import models
from user.models import Employee, Department
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=350)
    description = models.CharField(max_length=450)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=350)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField()
    category = models.CharField(max_length=220)

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    type = models.CharField(max_length=350)


class Issue(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    title = models.CharField(null=True, blank=True,max_length=350)
    details = models.CharField(null=True, blank=True,max_length=350)
    cost = models.IntegerField(default=0)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    signature = models.CharField(null=True, blank=True,max_length=150)
    issued = models.BooleanField(default=False)
    issued_at = models.DateTimeField(auto_now=False, null=True, blank=True)

    def __str__(self):
        return f"{self.employee}_{self.book} book issue request"


class Docservice(models.Model):
    name = models.CharField(max_length=350)
    staff_id = models.IntegerField()
    title = models.CharField(null=True, blank=True, max_length=350)
    details = models.CharField(null=True, blank=True,max_length=350)
    service_type = models.CharField(max_length=350)
    department = models.CharField(max_length=350)
    pages = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    signature = models.CharField(null=True, blank=True,max_length=150)

    # AUTO FIELDS
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_type

