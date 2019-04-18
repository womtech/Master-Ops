from django.conf.urls import url, include
from . import views

urlpatterns = [
  url(r"^$", views.CFMSHome.as_view()),
  url("list", views.CFMSList.as_view()),
  url("contract_performance", views.CFMSReport_Contract.as_view()),
  url("partner_performance", views.CFMSReport_Partner.as_view()),
  url("platform_performance", views.CFMSReport_Platform.as_view()),
  url("asset_performance", views.CFMSReport_Asset.as_view()),
  url("affiliates_performance", views.CFMSReport_Affiliate.as_view()),
  url("contract_report_dv", views.CFMSReport_ContractReportDetail.as_view()),
  url("partner_report_dv", views.CFMSReport_PartnerReportDetail.as_view()),
]

# url(r"^$", views.)
