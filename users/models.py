from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail  

# Create your models here.

class User(AbstractUser):
    ADMIN = 'admin'
    CLIENT = 'client'
    HOST = 'host'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CLIENT, 'Client'),
        (HOST, 'Host'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email=models.CharField(max_length=255,unique=True)
    password=models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CLIENT)
    username=models.CharField(max_length=50,default=None)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
"""
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="KriTirank"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )"""
    
