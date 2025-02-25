from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    Fields:
        - id: Unique identifier for the booking.
        - user_name: The username of the user who made the booking (read-only).
        - movie_title: The title of the booked movie (read-only).
        - booking_date: The date and time of the booking.
        - num_tickets: The number of tickets booked.
        - total_price: The total cost of the booking (read-only).
        - showtime: The showtime of the movie (read-only).
    """
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    user_name = serializers.SerializerMethodField()
    showtime = serializers.DateTimeField(source='movie.showtime', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'user_name', 'movie_title', 'booking_date', 'num_tickets', 'total_price', 'showtime']
        read_only_fields = ['total_price']
    
    def get_user_name(self, obj):
        """ Retrieve the username of the user who made the booking """
        return obj.user.username
