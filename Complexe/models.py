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
    lattitude = models.DecimalField(max_digits = 30,decimal_places = 20)
    longtitude = models.DecimalField(max_digits = 30,decimal_places = 20)
    description = models.CharField(max_length=250,default=None)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    url = models.CharField(max_length=250,blank=True, null=True)    
    
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