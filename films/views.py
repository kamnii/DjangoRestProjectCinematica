from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import (MovieListSerializer, 
                          MovieDetailSerializer)
from. models import Movie

@api_view(['GET'])
def movie_list_api_view(request):
    movies = Movie.objects.all()
    data = MovieListSerializer(movies, many=True).data

    return Response(
        data=data,
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def movie_detail_api_view(request, id):

    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'error': 'Movie Not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    
    data = MovieDetailSerializer(movie).data
    return Response(data=data,
                    status=status.HTTP_200_OK)