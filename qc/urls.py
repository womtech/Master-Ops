from django.conf.urls import url, include
from . import views

urlpatterns = [
  url(r"^$", views.QCHome.as_view()),
  url("list", views.QCList.as_view()),
  url("update", views.QCList.update, name='update' ),
  url("filter", views.QCList.filter,name='filter'),
]

# url(r"^$", views.)
