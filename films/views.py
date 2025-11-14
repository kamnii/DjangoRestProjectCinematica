from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .serializers import (MovieListSerializer, 
                          MovieDetailSerializer,
                          MoviewValidateSerializer)
from. models import Movie

@api_view(['GET', 'POST'])
def movie_list_api_view(request):
    # step 1: Collect films from DB (QuerySet)
    movies = (Movie.objects.select_related('director')
              .prefetch_related('genres', 'reviews').all())

    #step 2: Reformat (Serialize) to List of dictionaries
    if request.method == "GET":
        data = MovieListSerializer(movies, many=True).data

        #step 3: Return Response
        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
    
    elif request.method == "POST":
        serializer = MoviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        is_active = serializer.validated_data.get('is_active')
        realease_year = serializer.validated_data.get('realease_year')
        rating_imdb = serializer.validated_data.get('rating_imdb')
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')

        with transaction.atomic():
            movie = Movie.objects.create(
                title=title,
                text=text,
                is_active=is_active,
                realease_year=realease_year,
                rating_imdb=rating_imdb,
                director_id=director_id,
            )
            movie.genres.set(genres)
            movie.save()

        return Response(data=MovieDetailSerializer(movie).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie Not Found!'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        data = MovieDetailSerializer(movie).data
        return Response(data=data,
                        status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = MoviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            movie.title = serializer.validated_data.get('title')
            movie.text = serializer.validated_data.get('text')
            movie.is_active = serializer.validated_data.get('is_active')
            movie.realease_year = serializer.validated_data.get('realease_year')
            movie.rating_imdb = serializer.validated_data.get('rating_imdb')
            movie.director_id = serializer.validated_data.get('director_id')
            movie.genres.set(serializer.validated_data.get('genres'))
            movie.save()
            
        return Response(data=MovieDetailSerializer(movie).data,
                        status=status.HTTP_201_CREATED)
    
    elif request.method == "DELETE":
        movie.delete()
        movies = Movie.objects.all()
        return Response(data=MovieListSerializer(movies).data,
                        status=status.HTTP_204_NO_CONTENT)
