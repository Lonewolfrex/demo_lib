# library_app/models.py
from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    CONDITION_CHOICES = [
        ('mint', 'Mint'),
        ('not-mint', 'Not Mint'),
    ]

    AGE_GROUP_CHOICES = [
        ('kids', 'Kids'),
        ('adult', 'Adult'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")

    original_mrp = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_new = models.BooleanField(default=False)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='mint')
    genre = models.CharField(max_length=100, blank=True, default="")
    age_group = models.CharField(max_length=10, choices=AGE_GROUP_CHOICES, default='adult')

    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    discount_percent = models.PositiveIntegerField(default=0)
    offer_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    available = models.BooleanField(default=True)

    donated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='donated_books'
    )

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
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    donated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.book:
            return f"{self.book.title} ({self.user.username})"
        return f"Donation by {self.user.username}"


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    purchased_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} purchased {self.book.title}"
