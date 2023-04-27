from rest_framework import serializers
from .models import User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name','last_name','role', 'email', 'password','profile_pic']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
        return instance