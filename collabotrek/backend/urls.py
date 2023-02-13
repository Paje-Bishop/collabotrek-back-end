from django.urls import path
from . import views


urlpatterns = [
    path('members/', views.members, name='members'),
    path('login/', views.login, name='login'),
    path('trips/<int:trip_id>/', views.trips, name='trips'),
    path('<str:obj_type>/<int:obj_id>/invitations/<int:del_id>/', views.invitations, name='invitations'),
    path('trips/<int:trip_id>/flights/<int:flight_id>/', views.flights, name='flights'),
    # path('flights/<int:flight_id>/)', views.flight_detail, name='flights_detail'),
    path('trips/<int:trip_id>/hotels/<int:hotel_id>/', views.hotels, name='hotels'),
    path('trips/<int:trip_id>/activities/<int:activity_id>/', views.activities, name='activities'),
    path('<str:obj_type>/<int:obj_id>/comments/<int:comment_id>/', views.comments, name='comments')
]