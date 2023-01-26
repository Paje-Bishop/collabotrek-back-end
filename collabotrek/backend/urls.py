from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    path('trips/', views.trips, name='trips'),
    path('invitations/', views.invitations, name='invitations'),
    path('flights/', views.flights, name='flights'),
    path('hotels/', views.hotels, name='hotels'),
    path('activities/', views.activities, name='activities')
]