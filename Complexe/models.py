from django.db import models
from users.models import User
# Create your models here.
class Ville(models.Model):
    name = models.CharField(max_length=100)
class Zone(models.Model):
    name = models.CharField(max_length=100)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
class ComplexeSportif(models.Model):
    name= models.CharField(max_length=100)
    adresse = models.CharField(max_length=250)
    lattitude = models.DecimalField(max_digits = 22,decimal_places = 20)
    longtitude = models.DecimalField(max_digits = 22,decimal_places = 20)
    description = models.CharField(max_length=250,default=None)
    city = models.CharField(max_length=100,default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    url = models.CharField(max_length=250, null=True)    
    
class CategoryTerrain(models.Model):
    typeTerrain = models.CharField(max_length=250)
    price = models.FloatField()
    area = models.IntegerField(blank=True, null=True)
    complexeSportif = models.ForeignKey(ComplexeSportif, on_delete=models.CASCADE,default=None)  
class Terrain(models.Model):
    name = models.CharField(max_length=100,default=None)
    rank = models.IntegerField(null=True, blank=True, default=None)
    number_of_players = models.IntegerField(blank=True, null=True)
    is_reserved = models.BooleanField(default=False)
    category = models.ForeignKey(CategoryTerrain, on_delete=models.CASCADE,default=None)
class Photo(models.Model):
    url = models.CharField(max_length=250)
    terrain = models.ForeignKey(Terrain, on_delete=models.CASCADE)
class Reservation(models.Model):
    date = models.DateField()
    startTime = models.CharField(max_length=100,default=None)
    endTime = models.CharField(max_length=100,default=None)
    terrain = models.ForeignKey(Terrain, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_rejected = models.CharField(max_length=100,default=None)
    # is_confirmed = models.BooleanField(default=False)
    # is_canceled = models.BooleanField(default=False)
    # is_done = models.BooleanField(default=False)
    # is_paid = models.BooleanField(default=False)
    # is_refused = models.BooleanField(default=False)
    # is_waiting = models.BooleanField(default=False)
    # is_rejected = models.BooleanField(default=False)
    # is_accepted = models.BooleanField(default=False)
    # is_expired = models.BooleanField(default=False)
    # is_canceled_by_complex = models.BooleanField(default=False)
    # is_canceled_by_user = models.BooleanField(default=False)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    date = models.DateTimeField()
    number_of_players_needed = models.IntegerField()
    description = models.TextField()
    terrain = models.ForeignKey(Terrain, on_delete=models.CASCADE)
    post_reservation = models.ForeignKey(Reservation,on_delete=models.CASCADE,default=None)

class Joined(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    accepted = models.CharField(max_length=100,default='Requested')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,default=None)