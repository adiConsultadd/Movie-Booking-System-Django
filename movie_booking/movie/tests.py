import pytest
from django.urls import reverse
from rest_framework import status
from .models import Movie
from django.db.utils import IntegrityError

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

@pytest.mark.movies
class TestMovies:
    """ Test cases for movie-related API endpoints """
    def test_list_movies(self, auth_client, create_movie, movie_data):
        """ Test retrieving a list of movies """
        create_movie(**movie_data)
        url = reverse('movie-list')
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        
    def test_create_movie_as_admin(self, admin_client, movie_data):
        """ Test that an admin can create a new movie """
        url = reverse('movie-list')
        response = admin_client.post(url, movie_data)
        assert response.status_code == status.HTTP_201_CREATED
        
    def test_create_movie_as_user(self, auth_client, movie_data):
        """ Test that a regular user cannot create a movie """
        url = reverse('movie-list')
        response = auth_client.post(url, movie_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_retrieve_movie(self, auth_client, create_movie, movie_data):
        """ Test retrieving details of a specific movie """
        movie = create_movie(**movie_data)
        url = reverse('movie-detail', args=[movie.id])
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == movie_data['title']
    
    def test_update_movie_as_admin(self, admin_client, create_movie, movie_data):
        """ Test that an admin can update a movie """
        movie = create_movie(**movie_data)
        url = reverse('movie-detail', args=[movie.id])
        updated_data = {**movie_data, 'title': 'Updated Movie'}
        response = admin_client.put(url, updated_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Movie'
    
    def test_update_movie_as_user(self, auth_client, create_movie, movie_data):
        """ Test that a regular user cannot update a movie """
        movie = create_movie(**movie_data)
        url = reverse('movie-detail', args=[movie.id])
        updated_data = {**movie_data, 'title': 'Updated Movie'}
        response = auth_client.put(url, updated_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_delete_movie_as_admin(self, admin_client, create_movie, movie_data):
        """ Test that an admin can delete a movie """
        movie = create_movie(**movie_data)
        url = reverse('movie-detail', args=[movie.id])
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_delete_movie_as_user(self, auth_client, create_movie, movie_data):
        """ Test that a regular user cannot delete a movie """
        movie = create_movie(**movie_data)
        url = reverse('movie-detail', args=[movie.id])
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_book_movie(self, auth_client, create_movie, movie_data):
        """ Test booking a movie """
        movie = create_movie(**movie_data)
        url = reverse('movie-book', args=[movie.id])
        response = auth_client.post(url)  
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['num_tickets'] == 1
        assert float(response.data['total_price']) == float(movie_data['price']) * 1

    def test_cancel_booking(self, auth_client, create_movie, movie_data):
        """ Test canceling a movie booking """
        movie = create_movie(**movie_data)
        book_url = reverse('movie-book', args=[movie.id])
        auth_client.post(book_url)
        cancel_url = reverse('movie-cancel', args=[movie.id])
        response = auth_client.delete(cancel_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
