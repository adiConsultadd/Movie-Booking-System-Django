from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    showtime = models.DateTimeField(help_text="Showtime for the movie")   

    def __str__(self):
        return self.title