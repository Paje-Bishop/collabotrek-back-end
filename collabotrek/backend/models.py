from django.db import models


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField("First Name", max_length=24)
    last_name = models.CharField("Last Name", max_length=24)
    username = models.CharField("Username", max_length=24)
    password = models.CharField("Password", max_length=24)
    email = models.EmailField("Email", max_length=24)
    registrationDate = models.DateField("Registration Date", auto_now_add=True)


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField("Trip Title", max_length=24)
    user = models.ManyToManyField(Member, through='Trip_Invite', related_name='trips')
    host = models.ForeignKey(Member, on_delete=models.CASCADE)

class Trip_Invite(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='trip_invites')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='invited_users')
    departure_city = models.CharField(max_length=50)

class Flight(models.Model):
    id = models.AutoField(primary_key=True)
    depart_city = models.CharField("Departure City", max_length=50)
    depart_date = models.DateField
    depart_time = models.CharField("Departure Time", max_length=10)
    arrival_city = models.CharField("Arrival City", max_length=50)
    arrive_date = models.DateField
    arrive_time = models.CharField("Arrival Time", max_length=10)
    price = models.CharField("Flight Price", max_length=24)
    layover_id = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="layovers")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    votes = models.IntegerField


class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Hotel Name", max_length=30)
    address = models.CharField("Hotel Address", max_length=75, null=True)
    price = models.CharField("Hotel Price", max_length=24)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    votes = models.IntegerField


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Activity Name", max_length=100)
    address = models.CharField("Activity Address", max_length=75, null=True)
    price = models.CharField("Activity Price", max_length=24)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    votes = models.IntegerField


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Member, on_delete=models.RESTRICT)
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, null=True, blank=True)
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, null=True, blank=True)
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, null=True, blank=True)
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, null=True, blank=True)
    parent_comment = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="child_comments")
    message = models.TextField
    post_date = models.DateTimeField(auto_now_add=True)
