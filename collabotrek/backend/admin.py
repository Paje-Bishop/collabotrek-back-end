from django.contrib import admin
from backend.models import Member, Trip, Trip_Invite, Flight, Hotel, Activity, Comment

admin.site.register(Member)
admin.site.register(Trip)
admin.site.register(Flight)
admin.site.register(Hotel)
admin.site.register(Activity)
admin.site.register(Comment)
admin.site.register(Trip_Invite)
