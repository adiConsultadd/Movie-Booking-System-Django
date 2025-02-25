from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie
from .serializers import MovieSerializer
from auth.permissions import IsAdmin
from booking.models import Booking
from booking.serializers import BookingSerializer
from django.shortcuts import get_object_or_404

class MovieViewSet(viewsets.ModelViewSet):
    """ Allows authenticated users to view movies, while only admins can create, update, or delete movies """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    def get_permissions(self):
        """
            Assign permissions based on the action.
            Admins can create, update, or delete movies, while authenticated users can only view them.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def book(self, request, pk=None):
        """
            Allow authenticated users to book a movie.
            The number of tickets defaults to 1 if not provided.
        """
        movie = self.get_object()
        num_tickets = request.data.get('num_tickets', 1)
        
        try:
            booking = Booking.objects.create(
                user=request.user,
                movie=movie,
                num_tickets=num_tickets,
                total_price=movie.price * num_tickets
            )
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {"error": "You already have a booking for this movie"},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['delete'])
    def cancel(self, request, pk=None):
        """
            Allow users to cancel their booking for a specific movie.
            Returns an error if no booking exists.
        """
        try:
            booking = Booking.objects.get(movie_id=pk, user=request.user)
            booking.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Booking.DoesNotExist:
            return Response(
                {"error": "No booking found for this movie"},
                status=status.HTTP_404_NOT_FOUND
            )
