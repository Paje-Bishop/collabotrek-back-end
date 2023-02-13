from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from backend.models import Trip, Member, Flight, Hotel, Activity, Trip_Invite, Comment
from rest_framework import status, permissions
from django.db.models.functions import Length

@api_view(['GET', 'POST', 'PATCH'])
@permission_classes([permissions.AllowAny])
def members(request):
    # permission_classes = (permissions.AllowAny,)

    if request.method == 'POST':
        new_user_data = request.data
        new_user = Member(
            first_name=new_user_data['first_name'],
            last_name=new_user_data['last_name'],
            password=new_user_data['password'],
            email=new_user_data['email']
        )
        new_user.save()
        user_data = Member.mem_dict(new_user)
        return Response(user_data, status=201)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    if request.method == 'POST':
        requested_member = Member.objects.filter(
            email=request.data['email'], password=request.data['password'])[0]
        if requested_member:
            memberData = Member.mem_dict(requested_member)
            return Response(memberData)
        else:
            return Response({"message": "Error occurred. This user does not exist."}, 404)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([permissions.AllowAny])
def trips(request, trip_id):
    if request.method == 'POST':
        new_data = request.data
        host_id = new_data['host']
        new_trip = Trip(
            title=new_data['title'],
            host=Member.objects.filter(id=host_id)[0]
        )
        new_trip.save()
        new_invite = Trip_Invite(
            member=Member.objects.filter(id=host_id)[0],
            trip=new_trip,
            pending=False
        )
        new_invite.save()
        return Response(request.data, status=201)
    if request.method == 'DELETE':
        instance = Trip.objects.filter(id=trip_id)
        instance.delete()
        return Response({"Message": "Nice one!"})


@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
@permission_classes([permissions.AllowAny])
def invitations(request, obj_type, obj_id, del_id=''):
    if request.method == 'POST':
        new_invite = Trip_Invite(
            member=Member.objects.filter(id=request.data['member'])[0],
            trip=Trip.objects.filter(id=request.data['trip'])[0],
            departure_city=request.data['departure_city'],
            pending=True
        )
        new_invite.save()
        return Response({"message": "You did it!!"}, status=201)
    if request.method == 'GET':
        if obj_type == 'trip':
            invitees = Trip.objects.filter(id=obj_id)[
                0].invited_users.all()
            invitee_list = []
            for member_invite in invitees:
                member = member_invite.member
                new_data = Member.mem_dict(member)
                new_data["departure_city"] = member_invite.departure_city
                new_data["invite_id"] = member_invite.id
                new_data["pending"] = member_invite.pending
                invitee_list.append(new_data)
            return Response(invitee_list)
        if obj_type == 'member':
            invited_trips = Member.objects.filter(id=obj_id)[
                0].trip_invites.all()
            trips_list = []
            for trip_invite in invited_trips:
                trip = trip_invite.trip
                new_data = {
                    "trip_id": trip.id,
                    "title": trip.title,
                    "departure_city": trip_invite.departure_city,
                    "pending": trip_invite.pending
                }
                trips_list.append(new_data)
            return Response(trips_list)
    if request.method == 'DELETE':
        if obj_type == 'member':
            del_trip = Trip.objects.filter(id=del_id)[0]
            invited_trip = Member.objects.filter(
                id=obj_id)[0].trip_invites.filter(trip=del_trip)
            invited_trip.delete()
            return Response({"Message": "Nice one!"})
    if request.method == 'PATCH':
        del_trip = Trip.objects.filter(id=del_id)[0]
        invited_trip = Member.objects.filter(
            id=obj_id)[0].trip_invites.filter(trip=del_trip)[0]
        invited_trip.pending = False
        invited_trip.save()
        return Response({"Message": "Nice one!"})


@api_view(['POST', 'DELETE'])
@permission_classes([permissions.AllowAny])
def comments(request, obj_type, obj_id, comment_id=''):
    if request.method == 'POST':
        new_comment = Comment(
            flight=Flight.objects.filter(id=obj_id)[
                0] if obj_type == 'flight' else None,
            hotel=Hotel.objects.filter(id=obj_id)[
                0] if obj_type == 'hotel' else None,
            activity=Activity.objects.filter(id=obj_id)[
                0] if obj_type == 'activity' else None,
            trip=Trip.objects.filter(id=obj_id)[
                0] if obj_type == 'trip' else None,
            author=Member.objects.filter(id=request.data['author'])[0],
            message=request.data['message'],
        )
        new_comment.save()
        if request.data['parent_comment']:
            parent=Comment.objects.filter(id=request.data['parent_comment'])[0]
            new_comment.parent_comment.add(parent)
        new_comment.save()
        return Response({"message": "You did it!!"}, status=201)
    if request.method == 'DELETE':
        comment = Comment.objects.filter(id=comment_id)
        comment.delete()
        return Response({"Message": "Nice one!"})


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([permissions.AllowAny])
def flights(request, flight_id='', trip_id=''):
    if request.method == 'POST':
        new_flight = Flight(
            depart_city=request.data['depart_city'],
            depart_date=request.data['depart_date'],
            depart_time=request.data['depart_time'],
            arrive_city=request.data['arrive_city'],
            arrive_date=request.data['arrive_date'],
            arrive_time=request.data['arrive_time'],
            price=request.data['price'],
            link=request.data['link'],
            trip=Trip.objects.filter(id=trip_id)[0]
        )
        new_flight.save()
        if request.data["layover_id"]:
            parent_flight = Flight.objects.filter(
                id=request.data['layover_id'])[0]
            new_flight.layover_id.add(parent_flight)
        return Response({"message": "You did it!!"}, status=201)
    if request.method == 'GET':
        flights_query = Trip.objects.filter(id=trip_id)[
            0].flight_set.all().order_by('voters')
        flight_list = []
        for flight in flights_query:
            flight_obj = Flight.flight_dict(flight)
            flight_list.append(flight_obj)
        return Response(flight_list)
    if request.method == 'PATCH':
        instance = Flight.objects.filter(id=flight_id)[0]
        member = Member.objects.filter(id=request.data['member'])[0]
        if request.data['vote'] == True:
            instance.voters.add(member)
            instance.save()
        if request.data['vote'] == False:
            instance.voters.remove(member)
            instance.save()
        return Response({"message": "you got it dude!"})
    if request.method == 'DELETE':
        flight = Flight.objects.filter(id=flight_id)
        flight.delete()
        return Response({"Message": "Nice one!"})


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([permissions.AllowAny])
def hotels(request, trip_id='', hotel_id=''):
    if request.method == 'POST':
        new_hotel = Hotel(
            name=request.data['name'],
            address=request.data['address'],
            price=request.data['price'],
            link=request.data['link'],
            trip=Trip.objects.filter(id=trip_id)[0]
        )
        new_hotel.save()
        return Response({"message": "You did it!!"}, status=201)
    if request.method == 'GET':
        hotels_query = Trip.objects.filter(id=trip_id)[
            0].hotel_set.all().order_by('voters')
        hotel_list = []
        for hotel in hotels_query:
            hotel_obj = Hotel.hotel_dict(hotel)
            hotel_list.append(hotel_obj)
        return Response(hotel_list)
    if request.method == 'PATCH':
        instance = Hotel.objects.filter(id=hotel_id)[0]
        member = Member.objects.filter(id=request.data['member'])[0]
        if request.data['vote'] == True:
            instance.voters.add(member)
            instance.save()
        if request.data['vote'] == False:
            instance.voters.remove(member)
            instance.save()
        return Response({"message": "whoa dude"})
    if request.method == 'DELETE':
        hotel = Hotel.objects.filter(id=hotel_id)
        hotel.delete()
        return Response({"Message": "Nice one!"})


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([permissions.AllowAny])
def activities(request, trip_id='', activity_id=''):
    if request.method == 'POST':
        new_activity = Activity(
            name=request.data['name'],
            address=request.data['address'],
            price=request.data['price'],
            link=request.data['link'],
            trip=Trip.objects.filter(id=trip_id)[0]
        )
        new_activity.save()
        return Response({"message": "You did it!!"}, status=201)
    if request.method == 'GET':
        activity_query = Trip.objects.filter(id=trip_id)[
            0].activity_set.all().order_by('voters')
        activity_list = []
        for activity in activity_query:
            activity_obj = Activity.activity_dict(activity)
            activity_list.append(activity_obj)
        return Response(activity_list)
    if request.method == 'PATCH':
        instance = Activity.objects.filter(id=activity_id)[0]
        member = Member.objects.filter(id=request.data['member'])[0]
        if request.data['vote'] == True:
            instance.voters.add(member)
            instance.save()
        if request.data['vote'] == False:
            instance.voters.remove(member)
            instance.save()
        return Response({"message": "whoa dude"})
    if request.method == 'DELETE':
        activity = Activity.objects.filter(id=activity_id)
        activity.delete()
        return Response({"Message": "Nice one!"})
