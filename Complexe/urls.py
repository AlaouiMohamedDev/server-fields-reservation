from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.apiOverview, name = 'api-overview'),
    path('complexe-list/', views.complexeList, name='complexe-list'),
    path('complexe-Id/<str:pk>/', views.complexeId, name='complexe-Id'),
    path('complexe-create/', views.complexeCreate, name='complexe-create'),
    path('complexe-update/<str:pk>/', views.complexeUpdate, name='complexe-update'),
    path('complexe-delete/<str:pk>/', views.complexeDelete, name='complexe-delete'),
    path('field-list/', views.fieldList, name='field-list'),
    path('field-Id/<str:pk>/', views.fieldId, name='field-Id'),
    path('field-create/', views.fieldCreate, name='field-create'),
    path('field-update/<str:pk>/', views.fieldUpdate, name='field-update'),
    path('field-delete/<str:pk>/', views.fieldDelete, name='field-delete'),
    path('fieldCategory-list/', views.fieldCategoryList, name='fieldCategory-list'),
    path('fieldCategory-Id/<str:pk>/', views.fieldCategoryId, name='fieldCategory-Id'),
    path('fieldCategory-create/', views.fieldCategoryCreate, name='fieldCategory-create'),
    path('fieldCategory-update/<str:pk>/', views.fieldCategoryUpdate, name='fieldCategory-update'),
    path('fieldCategory-delete/<str:pk>/', views.fieldCategoryDelete, name='fieldCategory-delete'),
    path('photo-list/', views.photoList, name='photo-list'),
    path('photo-Id/<str:pk>/', views.photoId, name='photo-Id'),
    path('photo-create/', views.photoCreate, name='photo-create'),
    path('photo-update/<str:pk>/', views.photoUpdate, name='photo-update'),
    path('photo-delete/<str:pk>/', views.photoDelete, name='photo-delete'),
    path('reservation-list/', views.reservationList, name='reservation-list'),
    path('reservation-Id/<str:pk>/', views.reservationId, name='reservation-Id'),
    path('reservation-create/', views.reservationCreate, name='reservation-create'),
    path('list_fields/', views.list_fields, name='list_fields'),
    ]
