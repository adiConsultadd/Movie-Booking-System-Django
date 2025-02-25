import pytest
from django.urls import reverse
from rest_framework import status
from .models import Booking
from movie.models import Movie

pytestmark = pytest.mark.django_db

@pytest.fixture
def movie_data():
    """ Fixture to provide sample movie data """
    return {
        'title': 'Test Movie',
        'description': 'Test Description',
        'release_date': '2025-02-24',
        'duration': 120,
        'price': '10.00',
        'showtime': '2025-02-24 14:30:00'
    }

@pytest.fixture
def create_movie(db):
    """ Fixture to create a movie instance """
    def make_movie(**kwargs):
        return Movie.objects.create(**kwargs)
    return make_movie

@pytest.fixture
def create_booking(db):
    """ Fixture to create a booking instance """
    def make_booking(user, movie, num_tickets=2, total_price=20.00):
        return Booking.objects.create(
            user=user,
            movie=movie,
            num_tickets=num_tickets,
            total_price=total_price
        )
    return make_booking

@pytest.mark.bookings
class TestBookings:
    """ Test cases for booking-related API endpoints """
    def test_list_bookings_as_admin(self, admin_client, create_booking, create_user, create_movie, movie_data):
        """ Test that an admin can retrieve a list of all bookings """
        user = create_user()
        movie = create_movie(**movie_data)
        create_booking(user=user, movie=movie)
        
        url = reverse('booking-list')
        response = admin_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['user_name'] == user.username

    def test_booking_history(self, api_client, create_booking, create_user, create_movie, movie_data):
        """ Test that an authenticated user can retrieve their booking history """
        user = create_user()
        api_client.force_authenticate(user=user)
        movie = create_movie(**movie_data)
        create_booking(user=user, movie=movie)
        
        url = reverse('booking-history')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['user_name'] == user.username

    def test_booking_history_no_bookings(self, api_client, create_user):
        """ Test that an authenticated user with no bookings receives an empty response """
        user = create_user()
        api_client.force_authenticate(user=user)
        
        url = reverse('booking-history')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_booking_list_unauthenticated(self, api_client):
        """ Test that an unauthenticated user cannot access the booking list """
        url = reverse('booking-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
