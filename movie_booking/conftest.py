import pytest
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """ Fixture to provide an instance of APIClient for making test requests """
    return APIClient()

@pytest.fixture
def user_data():
    """ Fixture to provide default user data"""
    return {
        'username': 'Alex',
        'password': 'alexmaha@123',
        'email': 'alex@example.com',
        'first_name': 'Adam',
        'last_name': 'Eve'
    }

@pytest.fixture
def admin_data():
    """ Fixture to provide default admin user data """
    return {
        'username': 'adminuser',
        'password': 'adminpass123',
        'email': 'admin@example.com',
        'first_name': 'Admin',
        'last_name': 'User',
        'is_staff': True
    }

@pytest.fixture
def create_user(db, user_data):
    """ Fixture to create a regular user """
    def make_user(**kwargs):
        if not kwargs:
            kwargs = user_data
        User.objects.filter(username=kwargs["username"]).delete()  
        user = User.objects.create_user(**kwargs)
        return user
    return make_user

@pytest.fixture
def create_admin(db, admin_data):
    """ Fixture to create an admin user """
    def make_admin(**kwargs):
        if not kwargs:
            kwargs = admin_data
        admin = User.objects.create_user(**kwargs)
        admin.is_staff = True
        admin.save()
        return admin
    return make_admin

@pytest.fixture
def auth_client(api_client, create_user):
    """ Fixture to provide an authenticated API client with a regular user """
    user = create_user()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client

@pytest.fixture
def admin_client(api_client, create_admin):
    """ Fixture to provide an authenticated API client with an admin user """
    admin = create_admin()
    refresh = RefreshToken.for_user(admin)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client
