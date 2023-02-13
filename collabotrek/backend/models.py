from django.db import models


def comment_list(cls, model_id):
    comment_query = cls.objects.filter(id=model_id)[0].comment_set.all()
    comment_list = []
    for comment in comment_query:
        comment_list.append(Comment.comment_dict(comment))
    return comment_list


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField("First Name", max_length=24)
    last_name = models.CharField("Last Name", max_length=24)
    password = models.CharField("Password", max_length=24)
    email = models.EmailField("Email", max_length=24)
    registrationDate = models.DateField("Registration Date", auto_now_add=True)

    def mem_dict(self):
        mem_data = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "email": self.email
        }
        return mem_data


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField("Trip Title", max_length=24)
    user = models.ManyToManyField(
        Member, through='Trip_Invite', related_name='trips')
    host = models.ForeignKey(Member, on_delete=models.CASCADE)

    def trip_dict(self):
        trip_data = {
            "id": self.id,
            "title": self.title
        }


class Trip_Invite(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='trip_invites')
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, related_name='invited_users')
    departure_city = models.CharField(max_length=50, null=True, blank=True)
    # inviter = models.ForeignKey(
    #     Member, on_delete=models.CASCADE, related_name='trip_inviting')
    pending = models.BooleanField(blank=True)


class Flight(models.Model):
    id = models.AutoField(primary_key=True)
    depart_city = models.CharField("Departure City", max_length=50)
    depart_date = models.DateField(blank=True, null=True)
    depart_time = models.CharField("Departure Time", max_length=10)
    arrive_city = models.CharField("Arrival City", max_length=50)
    arrive_date = models.DateField(blank=True, null=True)
    arrive_time = models.CharField("Arrival Time", max_length=10)
    price = models.CharField("Flight Price", max_length=24)
    layover_id = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="layovers")
    trip = models.ForeignKey(
        Trip, on_delete=models.CASCADE, null=True, blank=True)
    voters = models.ManyToManyField(
        Member, through='Vote_Status', related_name='flights_voted')
    link = models.CharField("link", max_length=500, blank=True, null=True)
    
    def layover_list(self):
        layovers = Flight.objects.filter(layover_id=self.id)
        ids = []
        for layover in layovers:
            ids.append(layover.id)
        return ids

    def flight_dict(self):
        layovers = Flight.layover_list(self)
        voter_ids = [x.id for x in self.voters.all()]

        flight_data = {
            "id": self.id,
            "depart_city": self.depart_city,
            "depart_date": self.depart_date,
            "depart_time": self.depart_time,
            "arrive_city": self.arrive_city,
            "arrive_date": self.arrive_date,
            "arrive_time": self.arrive_time,
            "price": self.price,
            "layovers": layovers,
            "comments": comment_list(Flight, self.id),
            "voters": voter_ids,
            "link": self.link
        }
        return flight_data


class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Hotel Name", max_length=30)
    address = models.CharField("Hotel Address", max_length=75, null=True)
    price = models.CharField("Hotel Price", max_length=24)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    voters = models.ManyToManyField(
        Member, through='Vote_Status', related_name='hotel_voted')
    link = models.CharField("link", max_length=500, blank=True, null=True)


    def hotel_dict(self):
        voter_ids = [x.id for x in self.voters.all()]
        hotel_data = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "price": self.price,
            "comments": comment_list(Hotel, self.id),
            "voters": voter_ids,
            "link": self.link
        }
        return hotel_data


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Activity Name", max_length=100)
    address = models.CharField("Activity Address", max_length=75, null=True)
    price = models.CharField("Activity Price", max_length=24)
    date = models.DateField(blank=True, null=True, default="1900-01-01")
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    voters = models.ManyToManyField(
        Member, through='Vote_Status', related_name='activity_voted')
    link = models.CharField("link", max_length=500, blank=True, null=True)

    def activity_dict(self):
        voter_ids = [x.id for x in self.voters.all()]
        activity_data = {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "price": self.price,
            "date": self.date,
            "comments": comment_list(Activity, self.id),
            "voters": voter_ids,
            "link": self.link
        }
        return activity_data

class Vote_Status(models.Model):
    voter = models.ForeignKey(
        Member, on_delete=models.PROTECT, related_name='vote_history')
    flight = models.ForeignKey(
        Flight, on_delete=models.PROTECT, blank=True, null=True, related_name='voted')
    hotel = models.ForeignKey(
        Hotel, on_delete=models.PROTECT, blank=True, null=True, related_name='voted')
    activity = models.ForeignKey(
        Activity, on_delete=models.PROTECT, blank=True, null=True, related_name='voted')

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
    message = models.CharField(
        "Message", max_length=240, default="Comment Error")
    post_date = models.DateTimeField(auto_now_add=True)

    def child_list(self):
        comments = Comment.objects.filter(parent_comment=self.id)
        author_name = self.author.first_name
        children = []
        for child in comments:
            comment_data = {
                "id": child.id,
                "message": child.message,
                "post_date": child.post_date,
                "author": author_name,
                "child_comments": Comment.child_list(child)
            }
            children.append(comment_data)
        return children

    def comment_dict(self):
        author_name = self.author.first_name
        comment_data = {
            "id": self.id,
            "message": self.message,
            "post_date": self.post_date,
            "author": author_name,
            "child_comments": Comment.child_list(self)
        }
        return comment_data
