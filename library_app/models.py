# library_app/models.py
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rented_on = models.DateTimeField(auto_now_add=True)
    returned_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    donated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book_title} ({self.user.username})"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchased_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} purchased {self.book.title}"
