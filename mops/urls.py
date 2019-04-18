from django.conf.urls import url, include
from django.contrib import admin
from authme import views

admin.site.site_header = "Master Ops"
admin.site.site_title = "Master Ops"
admin.site.index_title = "Administration"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('home.urls')),
    url(r'^authme', include(('authme.urls','authme'), namespace='authme')),
    url(r'^qc/', include('qc.urls')),
    url(r'^ytm/', include('ytm.urls')),
    url(r'^onemusic/', include('onemusic.urls')),
    url(r'^kpt/', include('kpt.urls')),
    url(r'^onemusic/', include('onemusic.urls')),
    url(r'^dam/', include('dam.urls')),
    url(r'^cfms/', include('cfms.urls')),
#    url(r'^asset/', include('asset.urls')),
]

