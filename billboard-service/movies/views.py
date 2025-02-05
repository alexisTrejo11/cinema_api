from rest_framework import viewsets
from .models import Cinema, Theater, Movie, Showtime
from .serializers import CinemaSerializer, TheaterSerializer, MovieSerializer, ShowtimeSerializer
from rest_framework.decorators import action
from rest_framework import viewsets, filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .service.showtime_service import ShowTimeService
from .utils.movie_filter import MovieFilter
from .utils.show_time_filter import ShowtimeSearchFilter


class CinemaViewSet(viewsets.ModelViewSet):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer


class TheaterViewSet(viewsets.ModelViewSet):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'theater_type']  
    ordering_fields = ['capacity', 'name']


    @action(detail=False, methods=['get'])
    def search(self, request):
        name = request.query_params.get('name', None)
        if name:
            theaters = self.queryset.filter(name__icontains=name)
            serializer = self.get_serializer(theaters, many=True)
            return Response(serializer.data)
        return Response({"error": "Query parameter 'name' not provided"}, status=400)


    @action(detail=False, methods=['get'])
    def filter_by_type(self, request):
        theater_type = request.query_params.get('type', None)
        if theater_type:
            theaters = self.queryset.filter(theater_type=theater_type)
            serializer = self.get_serializer(theaters, many=True)
            return Response(serializer.data)
        return Response({"error": "Query parameter 'type' not provided"}, status=400)

    @action(detail=False, methods=['get'])
    def in_maintenance(self, request):
        theaters = self.queryset.filter(maintenance_mode=True)
        serializer = self.get_serializer(theaters, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_cinema(self, request):
        cinema_id = request.query_params.get('cinema_id', None)
        if cinema_id:
            theaters = self.queryset.filter(cinema_id=cinema_id)
            serializer = self.get_serializer(theaters, many=True)
            return Response(serializer.data)
        return Response({"error":  "Query parameter 'cinema_id' not provided"}, status=400)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        title = request.query_params.get('title', None)
        duration = request.query_params.get('duration', None)
        genre = request.query_params.get('genre', None)
        rating = request.query_params.get('rating', None)
        end_date = request.query_params.get('end_date', None)
        is_active = request.query_params.get('is_active', None)
    
        movie_filter = MovieFilter()
        if title:
            movie_filter.add_title(title)
        if duration:
            movie_filter.add_duration(duration)
        if genre:
            movie_filter.add_genre(genre)
        if rating:
            movie_filter.add_rating(rating)
        if end_date:
            movie_filter.add_end_date(end_date)
        if is_active is not None:
            movie_filter.add_is_active(is_active)

        filter_criteria = {k: v for k, v in vars(movie_filter.build()).items() if v is not None}
        
        movies = Movie.objects.filter(**filter_criteria)
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)


class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.all()
    serializer_class = ShowtimeSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        try:
            filter_builder = ShowtimeSearchFilter()
            filter_builder.by_cinema(request.query_params.get('cinema_id'))
            filter_builder.by_movie(request.query_params.get('movie_id'))
            filter_builder.by_theater(request.query_params.get('theater_id'))
            filter_builder.by_start_time(request.query_params.get('start_time'))
            filter_builder.by_end_time(request.query_params.get('end_time'))            
            filters = filter_builder.build()

            queryset = Showtime.objects.all()

            if 'cinema_id' in filters:
                queryset = queryset.filter(theater__cinema_id=filters['cinema_id'])

            if 'movie_id' in filters:
                queryset = queryset.filter(movie=filters['movie_id'])

            if 'theater_id' in filters:
                queryset = queryset.filter(theater=filters['theater_id'])

            if 'start_time' in filters:
                queryset = queryset.filter(start_time__gte=filters['start_time'])

            if 'end_time' in filters:
                queryset = queryset.filter(end_time__lte=filters['end_time'])

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        showtime_service = ShowTimeService()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            showtime_service.validate_persistence(serializer.validated_data)

            return super().create(request, *args, **kwargs)
        
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        showtime_service = ShowTimeService()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            showtime_service.validate_persistence(serializer.validated_data, is_update=True)
            return super().update(request, *args, **kwargs)
        
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)