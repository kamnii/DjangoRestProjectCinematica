from django.contrib import admin
from films.models import Movie, Director, Genre, Review


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Director)
admin.site.register(Genre)
