from django.contrib import admin
from django.urls import path
from films import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/movies/', views.movie_list_api_view),
    path('api/v1/movies/<int:id>/', views.movie_detail_api_view)
]
