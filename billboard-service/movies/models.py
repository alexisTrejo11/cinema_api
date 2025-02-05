from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

class Cinema(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    tax_number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Theater(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='theaters')
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    theater_type = models.CharField(
        max_length=20,
        choices=[
            ('2D', '2D'),
            ('3D', '3D'),
            ('IMAX', 'IMAX'),
            ('4DX', '4DX'),
            ('VIP', 'VIP'),
        ]
    )
    is_active = models.BooleanField(default=True)
    maintenance_mode = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cinema.name} - {self.name}"


class Movie(models.Model):
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200, blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    genre = models.CharField(max_length=100, choices=[
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('romance', 'Romance'),
        ('thriller', 'Thriller'),
        ('drama', 'Drama'),
        ('sci-fi', 'Science Fiction'),
    ])
    rating = models.CharField(
        max_length=10,
        choices=[
            ('G', 'General Audience'),
            ('PG', 'Parental Guidance'),
            ('PG-13', 'Parental Guidance 13'),
            ('R', 'Restricted'),
            ('NC-17', 'Adults Only'),
        ]
    )
    poster_url = models.URLField(blank=True)
    trailer_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)  # Auto-calculate based on movie duration
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def save(self, *args, **kwargs):
        # Auto-calculate end_time
        if not self.end_time:
            duration = self.movie.duration
            self.end_time = self.start_time + timedelta(minutes=duration)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.movie.title} at {self.start_time}"
    
    @property
    def cinema(self):
        return self.theater.cinema
