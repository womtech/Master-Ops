import sys, json
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from libraries.PostgreSQLConnector import PostgreSQLConnector

class Platform_Performance_Report:

  def __init__(self):
    self.psy = PostgreSQLConnector()
    self.Columns = ['plat_id','platform_name','gross_earning','month']

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

    if CUSTOM_FILTERS:
      filter_str = parse_qs( CUSTOM_FILTERS )
      if 'f_daterange' in filter_str:
        dt_range = filter_str['f_daterange']
        s = dt_range[0].split(" - ")
        START_DATE = s[0]
        END_DATE = s[1]

    if ( VIEW_TYPE == "lifetime" ):
      SUB_QUERY = MONTH_GROUPING = ""
    elif ( VIEW_TYPE == "monthly"):
      SUB_QUERY = " , to_char(ce.month, 'Mon YYYY') as month "
      MONTH_GROUPING = " ,to_char(ce.month, 'Mon YYYY') "

    QUERY = '''
      select gp.plat_id as platform_id, sum(ce.revenue) as gross_earning, gp.platform_name as platform_name %s from cfms_earning as ce 
      join generic_platform as gp on gp.plat_id = ce.platform_id_id where ce.month > '%s' and ce.month < '%s' and 
      gp.platform_name like '%%%s%%' group by gp.platform_name, gp.plat_id %s order by %s %s LIMIT %d OFFSET %d
    ''' % ( str(SUB_QUERY) ,str(START_DATE), str(END_DATE), str(SEARCH), str(MONTH_GROUPING) ,str(ORDER), str(ORDER_DIR), int(LENGTH), int(START) )
    print (QUERY)
    result = self.psy._custom( QUERY, "select", "named_tuple" )

    if ( len(result['data']) == 0 ):
      return {"data":[], "draw":DRAW, "recordsTotal":0,"recordsFiltered":0}

    data = []
    for item in result['data']:
      T={}
      T['id'] = item.platform_id
      T['platform_code'] = item.platform_id
      T['platform_name'] = item.platform_name
      T['gross_earning'] = item.gross_earning
      if ( VIEW_TYPE == "monthly"):
        T['month'] = item.month
      data.append(T)
    return {"data":data, "draw":DRAW,"recordsTotal":result['count'], "recordsFiltered": result['count'] }

