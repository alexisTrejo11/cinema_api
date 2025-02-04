from django.contrib import admin
from django.urls import path

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movies.views import CinemaViewSet, TheaterViewSet, MovieViewSet, ShowtimeViewSet

router = DefaultRouter()
router.register(r'cinemas', CinemaViewSet)
router.register(r'theaters', TheaterViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'showtimes', ShowtimeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', include(router.urls)),
]
