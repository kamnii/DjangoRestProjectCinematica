from rest_framework import serializers
from .models import Movie, Director, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'first_name', 'last_name', 'age']


class MovieListSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    genre_list = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'reviews', 'director', 'genre_list', 'title', 'realease_year', 'is_active']
        depth = 1

    def get_genre_list(self, movie):
        return [i.name for i in movie.genre.all()]


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
