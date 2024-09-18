from django.db import models

# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200, unique=True)  # Ensure title uniqueness
    publisher = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    is_borrowed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('title', 'publisher')  # Enforce combination uniqueness


class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    due_date = models.DateField()

    class Meta:
        unique_together = ('user', 'book') 
