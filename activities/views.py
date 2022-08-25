from os.path import basename

import gpxpy
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ActivityForm, ImportGPXFileForm
from .models import Activity, ActivityType


class ActivityListView(ListView):
    model = Activity
    context_object_name = 'activities'


class ActivityDetailView(DetailView):
    model = Activity
    context_object_name = 'activity'


class ActivityEditView(ActivityDetailView):
    form_class = ActivityForm
    template_name = 'activities/activity_edit.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.get_object())
        return render(request, self.template_name, {self.context_object_name: self.get_object(), 'form': form})

    def post(self, request, *_args, **_kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('activity', kwargs={'pk': form.instance.id}))
        else:
            return render(request, self.template_name, {self.context_object_name: self.get_object(), 'form': form})


class ActivityStreamView(ActivityDetailView):
    def get(self, request, *args, **kwargs):
        activity: Activity = self.get_object()
        activity_data = {
            # '@context': [
            #     "https://www.w3.org/ns/activitystreams",
            #     {"adv": "https://athx.us/ns/adventure#"},
            # ],
            '@id': activity.identifier,
            'name': activity.name,
            'type': activity.type.uri,
            'startTime': activity.start_time,
            'endTime': activity.end_time,
            'location': [
                {'name': location.name, 'type': location.type.name}
                for location in activity.location.all()
            ] + activity.tracks,
            'actor': [
                {'name': actor.name, 'type': actor.type.name}
                for actor in activity.actor.all()
            ],
            'attachment': [
                {
                    'type': 'Link',
                    'href': attachment.file.name,
                    'mediaType': attachment.media_type,
                    'rel': attachment.rel,
                }
                for attachment in activity.attachments.all()
            ]
        }
        return JsonResponse(activity_data)


class ActivityTracksView(ActivityDetailView):
    template_name = 'activities/activity_tracks.html'


class ImportGPXFileView(View):
    template_name = 'activities/import_gpx_file.html'

    def get(self, request, *args, **kwargs):
        form = ImportGPXFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ImportGPXFileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            gpx_file = form.cleaned_data['gpx_file']
            gpx_basename = basename(gpx_file.name).replace('.gpx', '')
            date, slug, activity_type = gpx_basename.split('.', 3)
            gpx = gpxpy.parse(gpx_file)
            start = gpx.tracks[0].segments[0].points[0]
            end = gpx.tracks[-1].segments[-1].points[-1]
            activity = Activity(
                type=ActivityType.objects.get(pk=form.cleaned_data['activity_type']),
                identifier=f'{date}.{slug}#{activity_type}',
                name=slug.replace('-', ' ').title(),
                start_time=start.time,
                end_time=end.time,
                gpx_file=gpx_file,
            )
            activity.save()
            return HttpResponseRedirect(reverse('edit_activity', kwargs={'pk': activity.id}))

