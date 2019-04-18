from django.conf.urls import url, include
from . import views

urlpatterns = [
  url(r"^$", views.DAMHome.as_view()),
  url("lookups",views.DAMLookups.as_view()),
  url("update",views.DAMLookups.update, name='update'),
  url("download", views.DAMLookups.download, name='download'),
  url('nudge', views.DAMLookups.nudge, name='nudge'),
  url('place_request', views.DAMLookups.place_request, name='place_request'),
]
