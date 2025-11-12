from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    realease_year = models.IntegerField()
    rating_imdb = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title