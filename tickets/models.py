from django.db import models

class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=20)
    date = models.DateField()

    def __str__(self):
        return self.hall
    
class Guest(models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    geust = models.ForeignKey(Guest , related_name="reser_geust" , on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie , related_name="reser_movie" , on_delete=models.CASCADE)