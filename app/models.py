from django.db import models
from django.utils import timezone


# Create your models here.
class Video(models.Model):
    FEATURED = 'FT'
    LECTURES = 'LC'
    QURAN = 'QR'
    DUAS = 'DU'
    STORIES = 'ST'

    CATEGORY_CHOICES = [
        (FEATURED, 'Featured'),
        (LECTURES, 'Lectures'),
        (QURAN, 'Qur\'an'),
        (DUAS, 'Duas'),
        (STORIES, 'Stories'),
    ]

    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=FEATURED)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='videos/')
    file = models.FileField(upload_to='videos/')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='books/')
    file = models.FileField(upload_to='books/')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Poster(models.Model):
    title = models.CharField(max_length=100, default='Untitled Poster')
    description = models.CharField(max_length=200, default='No description provided')
    image = models.ImageField(upload_to='posters/')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
