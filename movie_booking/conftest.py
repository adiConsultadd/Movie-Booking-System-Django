import pytest
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
 
@pytest.fixture
def user_data():
    return {
        'username': 'Alex',
        'password': 'alexmaha@123',
        'email': 'alex@example.com',
        'first_name': 'Adam',
        'last_name': 'Eve'
    }

@pytest.fixture
def admin_data():
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
    def make_user(**kwargs):
        if not kwargs:
            kwargs = user_data
        User.objects.filter(username=kwargs["username"]).delete()  
        user = User.objects.create_user(**kwargs)
        return user
    return make_user


@pytest.fixture
def create_admin(db, admin_data):
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
    user = create_user()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client

@pytest.fixture
def admin_client(api_client, create_admin):
    admin = create_admin()
    refresh = RefreshToken.for_user(admin)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client