from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r"^myitems/$", views.MyItems.as_view(), name="MyItems"),
    url(r"^$", views.Home.as_view(), name='home'),
]

handler400 = 'views.Home.error_400'
handler500 = 'views.Home.error_500'

