from django.conf.urls import url, include
from . import views
from authme  import views


urlpatterns = [
  url(r"^/$", views.Login.as_view(), name="Login"),
  url(r"^logout/$", views.Login.logout, name='logout'),
  url("ccheck", views.Login.ccheck, name="ccheck"),
]
