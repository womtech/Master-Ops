from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r"^$", views.YTMHome.as_view(), name='home'),
    url(r"upload/", views.YTUpload.as_view(), name="upload"),
]
