from django.db import models

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
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    
class Terrain(models.Model):
    name = models.CharField(max_length=100)
    rank = models.IntegerField()
    typeT = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    tarifT = models.CharField(max_length=250)
    complexeSportif = models.ForeignKey(ComplexeSportif, on_delete=models.CASCADE)
class Photo(models.Model):
    url = models.CharField(max_length=100)
    terrain = models.ForeignKey(Terrain, on_delete=models.CASCADE)

