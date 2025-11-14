from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Movie, Director, Review, Genre


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
    genres_list = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'reviews', 'director', 'genres_list', 'title', 'realease_year', 'is_active']
        depth = 1

    def get_genres_list(self, movie):
        return [i.name for i in movie.genres.all()]


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MoviewValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    text = serializers.CharField(default="")
    is_active = serializers.BooleanField(default=True)
    realease_year = serializers.IntegerField(min_value=1900)
    rating_imdb = serializers.FloatField(min_value=1, max_value=10)
    director_id = serializers.IntegerField(min_value=1)
    genres = serializers.ListField(child=serializers.IntegerField(min_value=1), min_length=1)

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist')
        return director_id
        
    def validate_genres(self, genres):
        genres_db = Genre.objects.filter(id__in=genres)

        if len(genres) != len(genres_db):
            raise ValidationError('Genres does not exist')
        return genres
