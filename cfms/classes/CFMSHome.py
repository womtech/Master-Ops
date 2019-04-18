import sys, json
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from libraries.PostgreSQLConnector import PostgreSQLConnector

class CFMSHome:

  def __init__(self):
    self.psy = PostgreSQLConnector()
    self.Columns = ['contract_code','total_revenue','month']
    self.Contract_Status = ['','Active','Inactive','Draft']

  def get_date_string( self, date_str , option ):
    dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
    if option=="first_day_of_month":
      return str(dt_obj.year)+"-"+str(dt_obj.month)+"-01"
    elif option == "last_day_of_month":
      next_month = dt_obj.replace(day=28) + timedelta(days=4)
      return str(next_month - timedelta(days=next_month.day))

  def get_home_stats(self, request):
    DRAW = request.POST.get("draw", 1 )
    ORDER = self.Columns[int(request.POST.get("order[0][column]", 1 ))]
    ORDER_DIR = request.POST.get("order[0][dir]","desc")
    START = request.POST.get("start",0)
    LENGTH = request.POST.get("length",10)
    SEARCH = str(request.POST.get("search[value]",""))
    USERID = request.user.id
    VIEW_TYPE = request.POST.get("view_type","lifetime")
    CUSTOM_FILTERS = request.POST.get("custom_filter", False)
    START_DATE = self.get_date_string( request.POST.get('start_date','1991-08-07'), "first_day_of_month")
    END_DATE = self.get_date_string( request.POST.get('end_date',datetime.today().strftime("%Y-%m-%d")),"last_day_of_month")
    C_STATUS = 0
    CONTRACT_STATUS_STR = ''' and cc.contract_status ~ '%s' ''' % ( self.Contract_Status[0] )

    if CUSTOM_FILTERS:
      CONTRACT_STATUS_STR = ''' and cc.contract_status ~ '%s' ''' % ( self.Columns[C_STATUS] )
      filter_str = parse_qs( CUSTOM_FILTERS )
      contract_status = filter_str['contract_status'] if 'contract_status' in filter_str.keys() else ['0']
      CONTRACT_STATUS_STR = ''' and cc.contract_status ~ '%s' ''' % ( self.Contract_Status[int(contract_status[0])] )
      dt_range = filter_str['f_daterange']
      s = dt_range[0].split(" - ")
      START_DATE = s[0]
      END_DATE = s[1]

    if ( VIEW_TYPE == "lifetime" ):
      SUB_QUERY = MONTH_GROUPING = ""
    elif ( VIEW_TYPE == "monthly"):
      SUB_QUERY = " , TO_CHAR(ce.month, 'Mon YYYY') as month "
      MONTH_GROUPING = " ,to_char(ce.month, 'Mon YYYY') "

    QUERY = '''
      select ce.contract_id as contract_id, cc.code as contract_code, sum(ce.revenue) as total_revenue %s
      from cfms_earning as ce inner join cfms_contract as cc on ce.contract_id = cc.id where
      ce.month > '%s' and ce.month < '%s' and cc.code LIKE '%%%s%%' %s GROUP BY contract_id, contract_code %s ORDER BY %s %s  LIMIT %d OFFSET %d
    ''' % ( str(SUB_QUERY), str(START_DATE), str(END_DATE), str(SEARCH), CONTRACT_STATUS_STR , str(MONTH_GROUPING) ,str(ORDER), str(ORDER_DIR),int(LENGTH), int(START)  )

    result = self.psy._custom( QUERY, "select", "named_tuple" )

    if ( len(result['data']) == 0 ):
      return {"data":[], "draw":DRAW, "recordsTotal":0,"recordsFiltered":0}

    data = []
    for item in result['data']:
      T={}
      T['id'] = item.contract_id
      T['contract_code'] = item.contract_code
      T['total_revenue'] = item.total_revenue
      if ( VIEW_TYPE == "monthly"):
        T['month'] = item.month
      data.append(T)

    return {"data":data, "draw":DRAW,"recordsTotal":result['count'], "recordsFiltered": result['count'] }

