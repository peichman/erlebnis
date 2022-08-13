from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView

from .forms import ActivityForm
from .models import Activity


class ActivityListView(ListView):
    model = Activity
    context_object_name = 'activities'


class ActivityDetailView(DetailView):
    model = Activity
    context_object_name = 'activity'


class ActivityEditView(DetailView):
    form_class = ActivityForm
    model = Activity
    context_object_name = 'activity'
    template_name = 'activities/activity_edit.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.get_object())
        return render(request, self.template_name, {self.context_object_name: self.get_object(), 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=self.get_object())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('activity', kwargs={'pk': form.instance.id}))
        else:
            return render(request, self.template_name, {self.context_object_name: self.get_object(), 'form': form})


class ActivityTracksView(ActivityDetailView):
    template_name = 'activities/activity_tracks.html'


