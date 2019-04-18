from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.MusicHome.as_view()),
    url("reports", views.ReportsHome.as_view()),
]
