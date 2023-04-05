from django.urls import path
from . import views


urlpatterns = [
    path('Create/',views.complexCreate),
    path('Delete/<str:pk>/', views.complexDelete),
    path('Update/<str:pk>/',views.complexUpdate),
    path('Detail/<str:pk>/',views.complexDetails)
]