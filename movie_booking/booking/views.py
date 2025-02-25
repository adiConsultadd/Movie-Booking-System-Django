from rest_framework import viewsets, permissions
from .models import Booking
from .serializers import BookingSerializer
from auth.permissions import IsAdmin
from rest_framework.decorators import action
from rest_framework.response import Response

class BookingViewSet(viewsets.ReadOnlyModelViewSet):
    """ ViewSet for handling Booking-related API operations """
    serializer_class = BookingSerializer
    
    def get_permissions(self):
        """ Admins can list all bookings, while authenticated users can access their own bookings """
        if self.action == 'list':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """ Return queryset based on user permissions.
            Admins get all bookings, while users get only their own bookings.
        """
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def history(self, request):
        """ Retrieve booking history for the authenticated user """
        user = request.user
        bookings = Booking.objects.filter(user=user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
