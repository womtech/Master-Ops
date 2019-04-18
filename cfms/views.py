import sys
sys.path.insert(0, '/projects/mops/cfms/')
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse
from libraries.PostgreSQLConnector import PostgreSQLConnector
from libraries.packages.Permissions import PagePermissions
from classes.Contract_Performance_Report_DetailPage import Contract_Performance_Report_DetailPage
from classes.Partner_Performance_Report_DetailPage import Partner_Performance_Report_DetailPage
from classes.Partner_Performance_Report import Partner_Performance_Report
from classes.Contract_Performance_Report import Contract_Performance_Report
from classes.Platform_Performance_Report import Platform_Performance_Report
from classes.Asset_Performance_Report import Asset_Performance_Report
from django.http.response import JsonResponse
from django.core import serializers
from datetime import datetime, timedelta
import json, collections
from urllib.parse import urljoin

# Create your views here.
class CFMSReport_PartnerReportDetail ( View ):

  def get( self, request, *args, **kwargs):
    Obj = Partner_Performance_Report_DetailPage( 1 )
    pbi = Obj.getPartnerBasicInfo()
    ctl = Obj.getPartnerContracts()
    return render( request, "cfms/partner_report_dv.html",{"pbi":pbi["data"],"ctl":ctl["data"]});


class CFMSReport_Contract( View ):

  def get( self, request, *args, **kwargs):
    return render( request, "cfms/contract_performance_report.html")

  def post( self, request, *args, **kwargs ):
    CPR = Contract_Performance_Report()
    data = CPR.processMe(request)
    return JsonResponse( data , safe=False)


class CFMSReport_ContractReportDetail( View ):

  def get(self, request, *args, **kwargs):
    CONTRACT_ID = request.GET.get('ctr',False)
    if not CONTRACT_ID:
      return HttpResponse("Invalid URL")

    pgp = PagePermissions(request.path_info, request.user.id)
    view_contract_permission = pgp.check_raci( "contract",CONTRACT_ID)

    if not view_contract_permission:
      return HttpResponse("You don't have permission to view this contract")

    contracts = []
    contracts = pgp.get_raci( "contract" )

    Obj = Contract_Performance_Report_DetailPage( CONTRACT_ID )
    if not Obj.CheckIfContractExists():
      return HttpResponse("This contract doesn't exist")

    MonthSeries = Obj.MonthlyAggregateEarning()
    cmi = Obj.ContractInfo(  )
    signatories = Obj.ContractSignatories(  )
    rights_group = Obj.ContractRightsGroup(  )
    ct_overall = Obj.ContractOverallPerformanceReview( )

    return render( request, "cfms/contract_report_dv.html", {"ct_overall":ct_overall['data'],"contracts":contracts,"rights_group":rights_group['data'], "month_series": MonthSeries['data'], "cmi": cmi["data"], "signatories":signatories['data']})

  def post( self, request, *args, **kwargs):
    CONTRACT_ID = request.POST.get("custom_filter[ctr_data]",False)
    query_type = request.POST.get("custom_filter[query_type]",False)
    if not CONTRACT_ID:
      return JsonResponse([3],safe=False)

    pgp = PagePermissions( request.path_info, request.user.id )
    view_contract_permission = pgp.check_raci( "contract",CONTRACT_ID )

    if not view_contract_permission:
      return JsonResponse([2],safe=False)

    Obj = Contract_Performance_Report_DetailPage( CONTRACT_ID )

    if not Obj.CheckIfContractExists():
      return JsonResponse([1],safe=False)

    if query_type=="cols":
      return JsonResponse(Obj.getTableHeader(), safe=False)

    data = Obj.getGivenMonthRevBreakup( request )
    return JsonResponse(data, safe=False)


class CFMSReport_Partner( View ):

  def __init__(self):
    self.psy = PostgreSQLConnector()

  def post( self, request, *args, **kwargs ):
    PPR = Partner_Performance_Report()
    data = PPR.processMe(request);
    return JsonResponse( data , safe=False)

  def get( self, request, *args, **kwargs):
    return render( request, "cfms/partner_performance_report.html")

class CFMSReport_Platform( View ):
  def get( self, request, *args, **kwargs):
    return render( request, "cfms/platform_performance_report.html")

  def post(self, request, *args, **kwargs):
    PPR = Platform_Performance_Report()
    data = PPR.processMe ( request )
    return JsonResponse( data, safe = False)


class CFMSReport_Asset( View ):
  def post(self, request, *args, **kwargs):
    PPR = Asset_Performance_Report()
    data = PPR.processMe ( request )
    return JsonResponse( data, safe = False)

  def get( self, request, *args, **kwargs):
    return render( request, "cfms/asset_performance_report.html")

class CFMSReport_Affiliate( View ):
  def get( self, request, *args, **kwargs):
    return render( request, "cfms/contract_performance.html")

class CFMSHome( View ):
  def get(self,request,*args,**kwargs):
    QUERY_SUMMARY = '''select distinct((select count(id)  from cfms_contract where contract_status ~ 'Active' and start_date >= '2013-01-01' AND end_date <= '2020-01-01')) as Contracts,
      (select count(*) from asset_title where status = TRUE and added_on BETWEEN '2013-01-01' AND '2020-01-01') as Titles, 
      (select sum(calculated_revenue_usd) from cfms_earningsplit) as Top_Line_Revenue,
      (select sum(calculated_revenue_usd) from cfms_earningsplit where partner_id NOT IN (2,3)) as Gross_Revenue,
      (select sum(calculated_revenue_usd) from cfms_earningsplit where partner_id IN (2,3)) as Partner_Revenue from cfms_contract as a;'''
    QUERY_OUTSTANDING_CONTRACTS = '''SELECT  cfms_contract.code,sum(cfms_earning.revenue) as a FROM cfms_contract
      INNER JOIN cfms_earning ON cfms_contract.id = cfms_earning.contract_id where cfms_contract.contract_status ~ 'Active'
      group by cfms_contract.code order by a desc limit 10;'''

    QUERY_OUTSTANDING_PLATFORMS = '''SELECT generic_platform.platform_name, sum(cfms_earning.revenue) as a
      FROM generic_platform INNER JOIN cfms_earning ON cfms_earning.platform_id_id = generic_platform.plat_id 
      group by generic_platform.plat_id order by a desc limit 10;'''

    QUERY_OUTSTANDING_PARTNER = '''SELECT extras_partner.partner_name, sum(cfms_earningsplit.calculated_revenue_usd) as a
      FROM extras_partner INNER JOIN cfms_earningsplit ON  cfms_earningsplit.partner_id = extras_partner.id group by extras_partner.id order by a desc limit 10;'''
    self.psy = PostgreSQLConnector()
    response_summary = self.psy._custom(QUERY_SUMMARY,"select","named_tuple")
    response_contracts_summary = self.psy._custom(QUERY_OUTSTANDING_CONTRACTS,"select",'named_tuple')
    response_platforms_summary = self.psy._custom(QUERY_OUTSTANDING_PLATFORMS,"select",'named_tuple')
    response_partner_summary = self.psy._custom(QUERY_OUTSTANDING_PARTNER,"select",'named_tuple')
    return render(request,"cfms/home.html", {'summary':response_summary['data'], 'rcs':response_contracts_summary['data'], 'rpls':response_platforms_summary['data'], 'rpas':response_partner_summary['data'] } )

class CFMSList( View ):
  def get(self, request, *args, **kwargs):
    return render(request,"cfms/list.html")
