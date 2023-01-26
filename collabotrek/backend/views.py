from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from backend.models import Trip, Member, Flight, Hotel, Activity, Trip_Invite, Comment


@api_view(['GET', 'POST', 'PATCH'])
def members(request):
    if request.method == 'POST':
        new_user_data = request.data
        new_user = Member(
            first_name=new_user_data['first_name'],
            last_name=new_user_data['last_name'],
            username=new_user_data['username'],
            password=new_user_data['password'],
            email=new_user_data['email']
        )
        new_user.save()
        return Response({"message": "Got some data!", "data": request.data}, status=201)
    if request.method == 'GET':
        all_members = Member.objects.all()
        member_list = []
        for member in all_members:
            new_data = {
                "id": member.id,
                "first_name": member.first_name,
                "last_name": member.last_name,
                "username": member.username,
                "password": member.password,
                "email": member.email
            }
            member_list.append(new_data)
        return Response(member_list)
    return Response({"message": "Hello, world!"})


@api_view(['GET', 'POST', 'PATCH'])
def trips(request):
    if request.method == 'POST':
        new_data = request.data
        host_id = new_data['host']
        new_trip = Trip(
            title=new_data['title'],
            host=Member.objects.filter(id=host_id)[0]
        )
        new_trip.save()
        return Response({"message": "Got some data!", "data": request.data}, status=201)


@api_view(['GET', 'POST'])
def invitations(request):
    if request.method == 'POST':
        new_invite = Trip_Invite(
            member=Member.objects.filter(id=request.data['member'])[0],
            trip=Trip.objects.filter(id=request.data['trip'])[0],
            departure_city=request.data['departure_city']
        )
        new_invite.save()
        return Response({"message": "You did it!!"}, status=201)
    if request.method == 'GET':
        if request.data['trip']:
            invitees = Trip.objects.filter(id=request.data['trip'])[
                0].invited_users.all()
            invitee_list = []
            for member_invite in invitees:
                member = member_invite.member
                new_data = {
                    "id": member.id,
                    "first_name": member.first_name,
                    "last_name": member.last_name,
                    "username": member.username,
                    "password": member.password,
                    "email": member.email,
                    "departure_city": member_invite.departure_city
                }
                invitee_list.append(new_data)
            return Response(invitee_list)
        if request.data['member']:
            invited_trips = Member.objects.filter(id=request.data['member'])[
                0].trip_invites.all()
            trips_list = []
            for trip_invite in invited_trips:
                trip = trip_invite.trip
                new_data = {
                    "id": trip.id,
                    "title": trip.title,
                    "departure_city": trip_invite.departure_city
                }
                trips_list.append(new_data)
            return Response(trips_list)


@api_view(['GET', 'POST', 'DELETE'])
def comments(request):
    if request.method == 'POST':
        new_comment = Comment(
            flight=Flight.objects.filter(id=request.data['flight_id'])[
                0] if request.data['hotel_id'] else None,
            hotel=Hotel.objects.filter(id=request.data['hotel_id'])[
                0] if request.data['hotel_id'] else None,
            activity=Activity.objects.filter(id=request.data['activity_id'])[
                0] if request.data['activity_id'] else None,
            trip=Trip.objects.filter(id=request.data['trip_id'])[
                0] if request.data['trip_id'] else None,
            author=Member.objects.filter(id=request.data['author'])[0],
            message=request.data['message'],
            parent_comment=Comment.objects.filter(id=request.data['parent_comment'])[
                0] if request.data['parent_comment'] else None
        )
        new_comment.save()
        return Response({"message": "You did it!!"}, status=201)


@api_view(['GET', 'POST', 'PATCH'])
def flights(request):
    if request.method == 'POST':
        new_flight = Flight(
            depart_city=request.data['depart_city'],
            depart_date=request.data['depart_date'],
            depart_time=request.data['depart_time'],
            arrival_city=request.data['arrival_city'],
            arrive_date=request.data['arrival_date'],
            arrive_time=request.data['arrival_time'],
            price=request.data['price'],
            layover_id=Flight.objects.filter(id=request.data['layover_id'])[
                0] if request.data['layover_id'] else None,
            votes=0,
            trip=Trip.objects.filter(id=request.data['trip'])[0]
        )
        new_flight.save()
        return Response({"message": "You did it!!"}, status=201)


@api_view(['GET', 'POST', 'PATCH'])
def hotels(request):
    if request.method == 'POST':
        new_hotel = Hotel(
            name=request.data['name'],
            address=request.data['address'],
            price=request.data['price'],
            votes=0,
            trip=Trip.objects.filter(id=request.data['trip'])[0]
        )
        new_hotel.save()
        return Response({"message": "You did it!!"}, status=201)


@api_view(['GET', 'POST', 'PATCH'])
def activities(request):
    if request.method == 'POST':
        new_activity = Activity(
            name=request.data['name'],
            address=request.data['address'],
            price=request.data['price'],
            votes=0,
            trip=Trip.objects.filter(id=request.data['trip'])[0]
        )
        new_activity.save()
        return Response({"message": "You did it!!"}, status=201)
