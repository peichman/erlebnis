from itertools import chain

import gpxpy
from django.db import models


class TypeBase(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=256)
    uri = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        else:
            return self is other


class ActivityType(TypeBase):
    pass


class PlaceType(TypeBase):
    pass


class ActorType(TypeBase):
    pass


class Place(models.Model):
    name = models.CharField(max_length=256)
    type = models.ForeignKey(PlaceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=256)
    type = models.ForeignKey(ActorType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Activity(models.Model):
    class Meta:
        verbose_name_plural = 'Activities'

    identifier = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    location = models.ManyToManyField(Place, blank=True)
    actor = models.ManyToManyField(Actor, blank=True)
    gpx_file = models.FileField(upload_to='gpx', null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gpx = None

    def __str__(self):
        if self.start_time is not None:
            return f'{self.type}: {self.name} ({self.start_time.date()})'
        else:
            return f'{self.type}: {self.name}'

    @property
    def gpx(self):
        if not self.gpx_file:
            return None
        if self._gpx is None:
            self._gpx = gpxpy.parse(self.gpx_file)
        return self._gpx

    @property
    def tracks(self):
        if self.gpx is None:
            return []
        locations = []
        for n, track in enumerate(self.gpx.tracks, 1):
            start_point = track.segments[0].points[0]
            end_point = track.segments[0].points[-1]
            prefix = f'Track {n} ' if len(self.gpx.tracks) > 1 else ''
            locations.extend((
                {
                    'type': 'Place',
                    'name': f'{prefix}Start',
                    'latitude': start_point.latitude,
                    'longitude': start_point.longitude,
                },
                {
                    'type': 'Place',
                    'name': f'{prefix}End',
                    'latitude': end_point.latitude,
                    'longitude': end_point.longitude,
                },
            ))
        bounds = self.gpx.get_bounds()
        locations.extend((
            {
                'type': 'Place',
                'name': 'Southwest Bounding Point',
                'latitude': bounds.min_latitude,
                'longitude': bounds.min_longitude,
            },
            {
                'type': 'Place',
                'name': 'Northeast Bounding Point',
                'latitude': bounds.max_latitude,
                'longitude': bounds.max_longitude,
            },
        ))
        return locations

    @classmethod
    def import_gpx(cls, file):
        gpx = gpxpy.parse(file)
        activity = cls()
        activity.name = gpx.name
        bounds = gpx.get_bounds()
        #gpx.tracks[0].segments[0].points
