from rest_framework import serializers
from .models import Ville, Zone, ComplexeSportif, Terrain, Photo, CategoryTerrain, Reservation, Post , Joined

class VilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ville
        fields = '__all__'

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'

class ComplexeSportifSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = ComplexeSportif
        fields = ['id', 'name', 'adresse','description','lattitude', 'longtitude', 'zone', 'user','url','city']
        read_only_fields = ['id']

class CategoryTerrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryTerrain
        fields = '__all__'
class TerrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terrain
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
class JoinedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joined
        fields = '__all__'