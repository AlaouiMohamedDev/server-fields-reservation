from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *

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
    path('reservation-update/<str:pk>/', views.reservationUpdate, name='reservation-update'),
    path('reservation-delete/<str:pk>/', views.reservationDelete, name='reservation-delete'),
    path('post-list/', views.postList, name='post-list'),
    path('post-Id/<str:pk>/', views.postId, name='post-Id'),
    path('post-create/', views.postCreate, name='post-create'),
    path('post-update/<str:pk>/', views.postUpdate, name='post-update'),
    path('post-delete/<str:pk>/', views.postDelete, name='post-delete'),
    path('list_fields/', views.list_fields, name='list_fields'),
    path('complexes/<int:complex_id>/terrains/', complex_terrains, name='complex-terrains'),
    path('utilisateur/<int:utilisateur_id>/complexes-sportifs/', complexe_sportif_utilisateur),
    path('reservations/', reservations, name='reservations'),
    path('reservations/<int:reservation_id>/status/', check_reservation_status, name='reservation-status'),
    path('completed_reservations_post/',completedReservations, name='completed-reservations'),
    path('approve-reservation/',approveReservation, name='approve-reservation'),
    path('fullReservations/', fullReservations, name='full-reservations'),
    path('reservations-status/', reservationsStatus, name='reservations-status'),
    path('join-match/', joinMatch, name='join-match'),
    path('list-joined/', listJoined, name='list-joined'),
    path('decrementPlayersNeeded/<str:pk>/', views.decrementPlayersNeeded, name='decrementPlayersNeeded'),
    path('rejectPlayer/<str:pk>/', views.rejectPlayer, name='rejectPlayer'),
    path('approve-host-account/<int:user_id>/', approve_host, name='approve_host_account'),
    path('reject-host-account/<int:user_id>/', reject_host, name='reject_host_account'),
    path('approvehost/<int:user_id>/', approveHosts, name='approve_complex'),
    path('rejecthost/<int:user_id>/', rejectHosts, name='reject_complex'),
    path('list_category_letter/',list_categories_FL, name='list_category_letter'),
    path('get_stats/', getStats, name='get_stats'),
    path('getCities_Scrapping/', getCititesScraping, name='getCities_Scrapping'),
    ]
