from rest_framework import serializers
from .models import Member, Trip, Flight, Hotel, Activity, Comment

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class MemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    registrationDate = serializers.DateField()

    class Meta:
        model = Member
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'registrationDate')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# class MemberSerializer(serializers.ModelSerializer):
#     """ Serializer class for Post model """

#     class Meta:
#         model = Member
#         fields = ('id', 'first_name', 'last_name', 'username', 'password', 'email')  
#         read_only_fields = ('id')  # Fields that are read-only

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
        