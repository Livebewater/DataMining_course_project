from django.db import models
import time


# Create your models here.

class Book(models.Model):
    isbn = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=70)
    author = models.CharField(max_length=30)
    # year_of_publication = models.DateField()
    year_of_publication = models.CharField(max_length=7)
    publisher = models.CharField(max_length=60)
    add_date = models.DateField(default=time.strftime("%Y-%m-%d", time.localtime()))
    mean_score = models.FloatField(default=0)
    image_url = models.CharField(default="", max_length=70)

    def __str__(self):
        return f"ISBN: {self.isbn} Title: {self.title}"


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=20)
    name = models.CharField(max_length=10, default="")
    password = models.CharField(max_length=8, default="")
    age = models.IntegerField()
    add_date = models.DateField(default=time.strftime("%Y-%m-%d", time.localtime()))

    def __str__(self):
        return f"User Record User-ID: {self.user_id} Location: {self.location} Age: {self.age}"


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    score = models.IntegerField(default=0)
    add_date = models.DateField(default=time.strftime("%Y-%m-%d", time.localtime()))

    def __str__(self):
        return f"Rate Record: User-ID: {self.user.user_id} ISBN: {self.book.isbn} Score: {self.score}"
