from django.db import models
from datetime import datetime


class Director(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def age(self):
        now = datetime.now().year
        return now - self.birthday.year


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Movie(models.Model):
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True)
    genres = models.ManyToManyField(Genre, null=True)
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True)
    is_active = models.BooleanField(blank=True)
    realease_year = models.IntegerField()
    rating_imdb = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

STARS = (
    (i, '* ' * i) for i in range(1, 11)
)


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    stars = models.IntegerField(choices=STARS, default=10)

    def __str__(self):
        return self.text
