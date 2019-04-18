from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from libraries.PostgreSQLConnector import PostgreSQLConnector
from django.http.response import JsonResponse
import json, csv, subprocess, functools as ft
from kpt.resources import HcpcResource, TrKeywordsResource
from import_export import resources
from tablib import Dataset
from kpt.models import Hcpc,TrendingKeywords
from wsgiref.util import FileWrapper

# Create your views here.
class KPTHome(View):
  def get(self,request,*args, **kwargs):
    self.psy = PostgreSQLConnector()
    QUERY_HCPC = "select keyword, cost_per_click from kpt_hcpc order by cost_per_click desc limit 20"
    hcpc_result = self.psy._custom( QUERY_HCPC, "select","named_tuple" )
    QUERY_HCPC_CNT = "select count(keyword) from kpt_hcpc"
    hcpc_cnt_result = self.psy._custom( QUERY_HCPC_CNT, "select","json" )
    QUERY_TCPC = "select keyword, cost_per_click from kpt_hcpc order by cost_per_click desc limit 20"
    tcpc_result = self.psy._custom( QUERY_TCPC, "select","named_tuple" )
    QUERY_TCPC_CNT = "select count(keyword) from kpt_hcpc"
    tcpc_cnt_result = self.psy._custom( QUERY_TCPC_CNT, "select","json" )
    return render(request, "kpt/home.html",{"hcpc": hcpc_result, "tcpc": tcpc_result, "hcpc_cnt_result": hcpc_cnt_result,"tcpc_cnt_result": tcpc_cnt_result})

class HighCPCKeywords(View):
  def __init__(self):
    self.psy = PostgreSQLConnector()

  def get(self, request, *args, **kwargs):
    return render(request, "kpt/high_cpc_keywords.html")

  def post(self, request, *args, **kwargs):
    draw = request.POST.get("draw", 1 )
    columns = request.POST.get("columns","")
    order = request.POST.get("order","")
    START = request.POST.get("start",0)
    LENGTH = request.POST.get("length",10)
    SEARCH = str(request.POST.get("search[value]",""))
    USERID = request.user.id
    _fields2hide = []
    Columns = []
    CURRENT_URL = '/kpt/hcpc'
    QUERY_COL = '''select sa.available_operations, sa.permission_str \
      from system_apps_assignment saa join system_user_form_level_permission sa \
      on saa.id=sa.app_assignment_id_fk_id where saa.user_id_fk_id = %d AND sa.form_url ='%s' ''' % ( USERID, CURRENT_URL )

    response = self.psy._custom( QUERY_COL, "select","named_tuple" )
    res_perm_fields = response['data'][0][1]

    for item in res_perm_fields:
      if item["perm"] != "hidden":
        l = [ item["perm"], item["ctype"], item["id"] ]
        p = {}
        p[ item["display_name"] ] = l
        p[ "title" ] = item["display_name"]
        Columns.append(p)

    for item in res_perm_fields:
        for key, val in item.items():
            if val == "hidden":
                _fields2hide.append(item['id'])

    t_data = self._formatData(_fields2hide, SEARCH, USERID, START, LENGTH, request )
    data_dump = json.dumps(t_data)
    data = json.loads(data_dump)
    if not data['data']:
      total_data = 0
    else:
      total_data = data['data'][0][-1]
      for j in data["data"]:
        j.pop()
    new_response = {"columns":Columns, "data":data['data'], "draw":draw, "recordsTotal":data['count'], "recordsFiltered":total_data}
    return JsonResponse( new_response, safe = False)

  def filterOutHiddenFields( self, FIELDS_TO_HIDE, SELECT_FIELDS_STR ):
    temp = SELECT_FIELDS_STR.replace(" ", "").split(",")
    for item in temp:
      t = item.split(".")
      if t[1] in FIELDS_TO_HIDE:
        temp.remove(item)
    return ','.join( temp)

  def _formatData( self, FIELDS_TO_HIDE, SEARCH, USERID, START, LENGTH, request ):
    SELECT_FIELDS_STR = '''keyword, volume, keyword_difficulty, cost_per_click, competitive_density, results, serp_features'''
    filter_flag = request.POST.get('filter')
    if filter_flag:
      v = request.POST
    else:
      WHERE = '''keyword like '%%%s%%' ''' % ( SEARCH )
    QUERY = '''SELECT %s, count(*) over() as full_count from kpt_hcpc where %s LIMIT %d OFFSET %d''' % (SELECT_FIELDS_STR, WHERE, int(LENGTH), int(START))
    response = self.psy._custom( QUERY.replace("\n"," ").replace("\r",""), "select", "named_tuple" )
    return response


class TrendingKeywords(View):
  def __init__(self):
    self.psy = PostgreSQLConnector()

  def get(self, request, *args, **kwargs):
    return render(request,"kpt/trending_keywords.html")

  def post(self, request, *args, **kwargs):
    draw = request.POST.get("draw", 1 )
    columns = request.POST.get("columns","")
    order = request.POST.get("order","")
    START = request.POST.get("start",0)
    LENGTH = request.POST.get("length",10)
    SEARCH = str(request.POST.get("search[value]",""))
    USERID = request.user.id
    _fields2hide = []
    Columns = []
    CURRENT_URL = '/kpt/tcpc'
    QUERY_COL = '''select sa.available_operations, sa.permission_str \
      from system_apps_assignment saa join system_user_form_level_permission sa \
      on saa.id=sa.app_assignment_id_fk_id where saa.user_id_fk_id = %d AND sa.form_url ='%s' ''' % ( USERID, CURRENT_URL )

    response = self.psy._custom( QUERY_COL, "select","named_tuple" )
    res_perm_fields = response['data'][0][1]

    for item in res_perm_fields:
      if item["perm"] != "hidden":
        l = [ item["perm"], item["ctype"], item["id"] ]
        p = {}
        p[ item["display_name"] ] = l
        p[ "title" ] = item["display_name"]
        Columns.append(p)

    for item in res_perm_fields:
        for key, val in item.items():
            if val == "hidden":
                _fields2hide.append(item['id'])
    t_data = self._formatData(_fields2hide, SEARCH, USERID, START, LENGTH, request )
    data_dump = json.dumps(t_data)
    data = json.loads(data_dump)
    if not data['data']:
      total_data = 0
    else:
      total_data = data['data'][0][-1]
      for j in data["data"]:
        j.pop()
    new_response = {"columns":Columns, "data":data['data'], "draw":draw, "recordsTotal":data['count'], "recordsFiltered":total_data}
    return JsonResponse( new_response, safe = False)

  def filterOutHiddenFields( self, FIELDS_TO_HIDE, SELECT_FIELDS_STR ):
    temp = SELECT_FIELDS_STR.replace(" ", "").split(",")
    for item in temp:
      t = item.split(".")
      if t[1] in FIELDS_TO_HIDE:
        temp.remove(item)
    return ','.join( temp)

  def _formatData( self, FIELDS_TO_HIDE, SEARCH, USERID, START, LENGTH, request ):
    SELECT_FIELDS_STR = '''keyword, volume, keyword_difficulty, cost_per_click, competitive_density, results, serp_features'''
    filter_flag = request.POST.get('filter')
    if filter_flag:
      v = request.POST
    else:
      WHERE = '''keyword like '%%%s%%' ''' % ( SEARCH )
    QUERY = '''SELECT %s, count(*) over() as full_count from kpt_trendingkeywords where %s LIMIT %d OFFSET %d''' % (SELECT_FIELDS_STR, WHERE, int(LENGTH), int(START))
    response = self.psy._custom( QUERY.replace("\n"," ").replace("\r",""), "select", "named_tuple" )
    return response


class UploadCsv(object):
  def uploadFile( request ):
    import_type =request.POST.get('import_type', False)
    file_name = request.FILES.get('file', False)
    if request.POST.get('download', False):
      file_wrapper  =  FileWrapper(open('./static/uploads/temp/sample.csv'))
      #tkresource = TrKeywordsResource()
      #dataset = tkresource.export()
      response = HttpResponse(file_wrapper, content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="sample.csv"'
      return response
    if file_name.name and import_type and not (file_name.name.endswith('.csv')):
      return JsonResponse({'message': 'only csv files are allowed'}, safe=False)
    else:
      data = request.FILES['file'].read().decode('utf-8')
      dataset = Dataset()
      imported_data = dataset.load( data, format='csv')
      if len(imported_data) == 0:
        return JsonResponse({'message': 'File is Empty' } , safe=False)
      else:
        header = ['keyword','volume','keyword_difficulty','cost_per_click','competitive_density','results','serp_features','date']
        if data.split('\n')[0].replace('"','').split(',') ==  header:
          if import_type == 'kpt_hcpc':
            model_name = HcpcResource()
          elif import_type == 'kpt_trendingkeywords':
            model_name = TrKeywordsResource()
          dataset.remove_duplicates()
          total_records = len(dataset)-1
          result = model_name.import_data(dataset, dry_run=True)
          model_name.import_data(dataset, dry_run=False)
          success_records = len(model_name.export())
          return JsonResponse({'total_records':str(total_records)+' successfully uploaded.', 'sucessfull_records':str(success_records)+'  of'}, safe=False)
        else:
          return JsonResponse({'message': 'Check the columns of your CSV file' } , safe=False)























'''
class UploadCsv(object):
  def __init__(self):
    self.psy = PostgreSQLConnector()

  def uploadFile( request ):
    import_type =request.POST.get('import_type', False)
    file_name = request.FILES.get('file', False)
    if not (import_type and  file_name):
      download =  request.POST.get('download', False)
      file_wrapper  =  FileWrapper(open('./static/uploads/temp/sample.csv'))
      response = HttpResponse(file_wrapper, content_type='text/csv')
      response['Content-Disposition'] = 'attachment; filename="sample.csv"'
      return response
    if file_name.name and (not file_name.name.endswith('.csv')):
      return JsonResponse({'message': 'only csv files are allowed'}, safe=False)
    if import_type   == 'kpt_hcpc':
      csvFilename   =  'tmp_hcpc.csv'
    elif import_type == 'kpt_trendingkeywords':
      csvFilename   =  'tmp_trendingKeywords.csv'
    psy = PostgreSQLConnector()
    records_list =list( map(lambda x: x.replace('"','').split(','), request.FILES['file'].read().decode('utf-8').split('\n'))) [:-1]
    csv.register_dialect('myDialect', quoting= csv.QUOTE_ALL, skipinitialspace= True )
    with open('./static/uploads/temp/'+csvFilename, 'w') as mycsvfile:
      writer = csv.writer(mycsvfile, dialect='myDialect')
      total_records = len([ writer.writerow(row)  for row in records_list ])-1
    data = csv.reader(open('./static/uploads/temp/'+ csvFilename, 'r'))
    next(data)'''
    #QUERY = '''insert into {table_name}(keyword,volume,keyword_difficulty,cost_per_click,competitive_density,results,serp_features,date) values {values}'''.format(table_name=import_type, values=ft.reduce(lambda a,b: str(a)+', '+str(b), map(lambda x: tuple(x),data) ) )
    #sucessfull_records = psy._custom(QUERY, 'update')['affected_rows']
    #return JsonResponse({'total_records':total_records, 'sucessfull_records':sucessfull_records}, safe=False)
