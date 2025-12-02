from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rented_on = models.DateTimeField(auto_now_add=True)
    returned_on = models.DateTimeField(null=True, blank=True)

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    donated_on = models.DateTimeField(auto_now_add=True)
