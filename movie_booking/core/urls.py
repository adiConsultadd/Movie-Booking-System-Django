from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth.urls')),
    path('api/movies/', include('movie.urls')),
    path('api/bookings/', include('booking.urls')),
]