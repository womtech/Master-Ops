import sys, json
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from libraries.PostgreSQLConnector import PostgreSQLConnector

class Partner_Performance_Report:

  def __init__(self):
    self.psy = PostgreSQLConnector()
    self.Columns = ['partner_code','partner_name','total_revenue','month','partner_status']
    self.Partner_Status = ["True","ep.is_active","not ep.is_active"]

  def get_date_string( self, date_str , option ):
    dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
    if option=="first_day_of_month":
      return str(dt_obj.year)+"-"+str(dt_obj.month)+"-01"
    elif option == "last_day_of_month":
      next_month = dt_obj.replace(day=28) + timedelta(days=4)
      return str(next_month - timedelta(days=next_month.day))

  def processMe(self, request):
    DRAW = request.POST.get("draw", 1 )
    ORDER = self.Columns[int(request.POST.get("order[0][column]", 2 ))]
    ORDER_DIR = request.POST.get("order[0][dir]","desc")
    START = request.POST.get("start",0)
    LENGTH = request.POST.get("length",10)
    SEARCH = str(request.POST.get("search[value]",""))
    USERID = request.user.id
    VIEW_TYPE = request.POST.get("view_type","lifetime")
    CUSTOM_FILTERS = request.POST.get("custom_filter", False)
    START_DATE = self.get_date_string( request.POST.get('start_date','1991-08-07'), "first_day_of_month")
    END_DATE = self.get_date_string( request.POST.get('end_date',datetime.today().strftime("%Y-%m-%d")),"last_day_of_month")
    PARTNER_STATUS_STR = self.Partner_Status[0]

    if CUSTOM_FILTERS:
      filter_str = parse_qs( CUSTOM_FILTERS )
      if 'f_daterange' in filter_str:
        dt_range = filter_str['f_daterange']
        s = dt_range[0].split(" - ")
        START_DATE = s[0]
        END_DATE = s[1]
      if 'partner_status' in filter_str:
        partner_status = filter_str['partner_status']
        PARTNER_STATUS_STR = self.Partner_Status[int(partner_status[0])]

    if ( VIEW_TYPE == "lifetime" ):
      SUB_QUERY = MONTH_GROUPING = ""
    elif ( VIEW_TYPE == "monthly"):
      SUB_QUERY = " , to_char(ce.month, 'Mon YYYY') as month "
      MONTH_GROUPING = " ,to_char(ce.month, 'Mon YYYY') "

    QUERY = '''
      select ces.partner_id as partner_id, ep.code as partner_code, ep.partner_name as partner_name, sum(ces.calculated_revenue_usd) as total_revenue, ep.is_active as partner_status %s from cfms_earning as ce 
      join cfms_earningsplit as ces on ce.id=ces.earning_ref_id join extras_partner as ep on ep.id = ces.partner_id 
      join cfms_contract as cc on cc.id = ce.contract_id where ce.month > '%s' and ce.month < '%s' and ep.partner_name like '%%%s%%' and %s 
      group by partner_id, partner_name, partner_code, ep.is_active %s order by %s %s LIMIT %d OFFSET %d
    ''' % ( str(SUB_QUERY) ,str(START_DATE), str(END_DATE), str(SEARCH), str(PARTNER_STATUS_STR),str(MONTH_GROUPING) ,str(ORDER), str(ORDER_DIR), int(LENGTH), int(START) )    
    result = self.psy._custom( QUERY, "select", "named_tuple" )

    if ( len(result['data']) == 0 ):
      return {"data":[], "draw":DRAW, "recordsTotal":0,"recordsFiltered":0}

    data = []
    for item in result['data']:
      T={}
      T['id'] = item.partner_id
      T['partner_code'] = item.partner_code
      T['partner_name'] = item.partner_name
      T['total_revenue'] = item.total_revenue
      T['partner_status'] = item.partner_status
      if ( VIEW_TYPE == "monthly"):
        T['month'] = item.month
      data.append(T)
    return {"data":data, "draw":DRAW,"recordsTotal":result['count'], "recordsFiltered": result['count'] }

