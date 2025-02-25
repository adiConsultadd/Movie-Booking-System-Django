import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db

@pytest.mark.auth
class TestAuthentication:
    def test_user_registration(self, api_client, user_data):
        """ Test that a user can register successfully. """
        user_data["password2"] = user_data["password"]
        response = api_client.post(reverse('register'), user_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'username' in response.data

    @pytest.mark.parametrize('invalid_field, invalid_value', [
        ('email', 'invalid-email'),
        ('password', '123'),  # Too short
        ('username', ''),  # Empty username
    ])
    def test_invalid_registration(self, api_client, user_data, invalid_field, invalid_value):
        """ Test that invalid registration data results in a 400 BAD REQUEST. """
        user_data[invalid_field] = invalid_value
        response = api_client.post(reverse('register'), user_data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_login(self, api_client, create_user, user_data):
        """ Test that a registered user can log in successfully. """
        create_user()
        response = api_client.post(reverse('login'), {
            'username': user_data['username'],
            'password': user_data['password']
        })
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
