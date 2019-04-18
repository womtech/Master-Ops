from django.conf.urls import url, include
from . import views

urlpatterns = [
  url(r"^$", views.KPTHome.as_view()),
  url("hcpc", views.HighCPCKeywords.as_view()),
  url("tcpc",views.TrendingKeywords.as_view()),
  url("fup",views.UploadCsv.uploadFile, name= '/kpt/fup'),
]
