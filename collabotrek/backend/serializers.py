from rest_framework import serializers
from .models import Member, Trip, Flight, Hotel, Activity, Comment

class MemberSerializer(serializers.ModelSerializer):
    """ Serializer class for Post model """

    class Meta:
        model = Member
        fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email')  
        read_only_fields = ('id')  # Fields that are read-only

class TripSerializer(serializers.ModelSerializer):
    """ Serializer class for Post model """

    class Meta:
        model = Trip
        fields = ('id', 'title', 'host')  
        read_only_fields = ('id')  # Fields that are read-only

class FlightSerializer(serializers.ModelSerializer):
    """ Serializer class for Post model """

    class Meta:
        model = Flight
        fields = ('id', 'title', 'author', 'content', 'published')  
        read_only_fields = ('id')  # Fields that are read-only

class HotelSerializer(serializers.ModelSerializer):
    """ Serializer class for Post model """

    class Meta:
        model = Hotel
        fields = ('id', 'title', 'author', 'content', 'published')  
        read_only_fields = ('id')  # Fields that are read-only

class ActivitySerializer(serializers.ModelSerializer):
    """ Serializer class for Post model """

    class Meta:
        model = Activity
        fields = ('id', 'title', 'author', 'content', 'published')  
        read_only_fields = ('id')  # Fields that are read-only

class CommentSerializer(serializers.ModelSerializer):
    """ Serializer class for Post model """

    class Meta:
        model = Comment
        fields = ('id', 'title', 'author', 'content', 'published')  
        read_only_fields = ('id')  # Fields that are read-only
        