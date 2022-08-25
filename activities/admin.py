from django.contrib import admin

from .models import Activity, ActivityType, Actor, ActorType, Place, PlaceType, Attachment

admin.site.register(Activity)
admin.site.register(ActivityType)
admin.site.register(Place)
admin.site.register(PlaceType)
admin.site.register(Actor)
admin.site.register(ActorType)
admin.site.register(Attachment)
