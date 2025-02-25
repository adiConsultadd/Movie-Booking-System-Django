from django.db import models
from django.contrib.auth.models import User
from movie.models import Movie

class Booking(models.Model):
    """ Model representing a movie booking  """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    num_tickets = models.IntegerField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        """ String representation of the booking, showing the username and movie title """
        return f"{self.user.username} - {self.movie.title}"
