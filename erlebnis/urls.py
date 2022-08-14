"""erlebnis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from activities.views import ActivityDetailView, ActivityEditView, ActivityListView, ActivityStreamView, \
    ActivityTracksView

urlpatterns = [
    path('activities/<int:pk>/json', ActivityStreamView.as_view(), name='activity_stream'),
    path('activities/<int:pk>/tracks/', ActivityTracksView.as_view(), name='activity_tracks'),
    path('activities/<int:pk>/edit/', ActivityEditView.as_view(), name='edit_activity'),
    path('activities/<int:pk>/', ActivityDetailView.as_view(), name='activity'),
    path('activities/', ActivityListView.as_view()),
    path('admin/', admin.site.urls),
]
