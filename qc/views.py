from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponse
from libraries.PostgreSQLConnector import PostgreSQLConnector
from django.http.response import JsonResponse
from django.core import serializers
from libraries.packages.Permissions import PagePermissions
import json

#QC Home Route
class QCHome( View ):

  def get(self, request, *args, **kwargs):
    self.psy = PostgreSQLConnector()

    QUERY_SUMMARY = '''SELECT distinct((SELECT COUNT(*) FROM qc_qclog WHERE qc_status=TRUE and qced_by_id = 1)) as Total_Qced, 
      (SELECT COUNT(*) FROM qc_qclog WHERE qc_status=FALSE and qced_by_id = 1) as Pending_QC, 
      (SELECT COUNT(*) FROM qc_qclog WHERE qced_by_id=1) as Total_Items, 
      (select count(*) from raci_property_ownership_channel_name_id_fk where property_ownership_id = 
      (select id as raci_po from raci_property_ownership where user_id_fk_id = 1)) as Total_CMS , 
      (select count(*) from raci_property_ownership_channel_name_id_fk as raci_yt_ch where raci_yt_ch.property_ownership_id = (select id from raci_property_ownership where user_id_fk_id = 1)) as Total_Channels FROM qc_qclog;'''

    QUERY_CHANNEL_SUMMARY_VIEW = '''select b.channel_name, max( CASE WHEN b.qc_status = 'TRUE' THEN count(b.*) ELSE 0 END ) AS QCED, 
      max( CASE WHEN b.qc_status = 'FALSE' THEN count(b.*) ELSE 0 END ) AS notQCED, 
      max( CASE WHEN b.qc_status IS NULL THEN count(b.*) ELSE 0 END ) AS notFlagged 
      from (select pc.channel_name, qc.qc_status, count(pyv.video_title) from raci_property_ownership_channel_name_id_fk as rpocn 
      join property_channel as pc on pc.id = rpocn.channel_id join property_youtube_videos as pyv on pyv.channel_id_fk_id = pc.id 
      full join qc_qclog as qc on qc.video_id_id = pyv.id where property_ownership_id IN 
      (select id from raci_property_ownership where user_id_fk_id = 1) group by qc.qc_status, pc.channel_name) as b group by b.channel_name'''

    QUERY_CMS_SUMMARY_VIEW = '''select b.cms_name, max( CASE WHEN b.qc_status = 'TRUE' THEN count(b.*) ELSE 0 END ) AS QCED, 
      max( CASE WHEN b.qc_status = 'FALSE' THEN count(b.*) ELSE 0 END ) AS notQCED, 
      max( CASE WHEN b.qc_status IS NULL THEN count(b.*) ELSE 0 END ) AS notFlagged 
      from (select pc.cms_name, qc.qc_status, count(pyv.video_title) from raci_property_ownership_cms_name_id_fk as rpocn 
      join property_cms as pc on pc.id= rpocn.cms_id join property_youtube_videos as pyv on pyv.channel_id_fk_id = pc.id 
      full join qc_qclog as qc on qc.video_id_id = pyv.id  where property_ownership_id IN 
      (select id from raci_property_ownership where user_id_fk_id = 1) group by qc.qc_status, pc.cms_name) as b group by b.cms_name'''
    response_summary = self.psy._custom(QUERY_SUMMARY,"select","named_tuple")
    response_channel_summary = self.psy._custom(QUERY_CHANNEL_SUMMARY_VIEW,"select",'named_tuple')
    response_cms_summary = self.psy._custom(QUERY_CMS_SUMMARY_VIEW,"select","named_tuple")

    return render(request,"qc/home.html", {'data':response_summary['data'], 'channel_view': response_channel_summary['data'], 'cms_view':response_cms_summary})

# Create your views here.
class QCList( View ):

  def __init__(self):
    self.psy = PostgreSQLConnector( )

  def filter( request ):
    flag = request.GET.get('filter')
    str = ""
    return JsonResponse(str, safe=False)

  def update( request ):
    USERID = request.user.id
    for key, value in request.POST.items():
      pass

    tCol = key.split("_")
    video_id = tCol.pop( )
    colName = "_".join( tCol )

    if colName == "moderator_remark":
      string = colName + " = '%s', remark_from_id = %d" % ( value, USERID )
    else:
      string = colName + " = '%s', qced_by_id = %d" % ( value.upper(), USERID )

    query2Update = "update qc_qclog set "+ string +"  where video_id_id IN (select id from property_youtube_videos where video_id ~ '%s')" % ( video_id )
    psy = PostgreSQLConnector( )
    response = psy._custom( query2Update,"update","json" )
    return JsonResponse( response, safe = False )

  def get( self, request, *args, **kwargs ):
    obj = PagePermissions( "/qc/list", request.user.id )
    response = obj.get_filter( )
    filters = obj.get_filter( )

    p_response = []
    for item in filters:
      temp = {}
      if item=="channel":
        QUERY = '''select a.channel_id, pc.channel_name from raci_property_ownership_channel_name_id_fk as a join property_channel as pc 
                on pc.id = a.channel_id where a.property_ownership_id IN (select id from raci_property_ownership where user_id_fk_id = 1)'''
        r = self.psy._custom( QUERY, "select", "json" )
        temp[item] = r["data"]
        p_response.append( temp )
      elif item=="cms":
        QUERY = '''select a.cms_id, pc.cms_name from raci_property_ownership_cms_name_id_fk as a join property_cms as pc on pc.id = a.cms_id
                where a.property_ownership_id IN (select id from raci_property_ownership where user_id_fk_id = 1)'''
        r = self.psy._custom( QUERY, "select","json" )
        temp[item] = r['data']
        p_response.append( temp )
      elif item=="qc_by":
        QUERY = '''select id, "first_name" || ' ' || "last_name" as user from auth_user'''
        r = self.psy._custom( QUERY, "select","json" )
        temp[item] = r['data']
        p_response.append( temp )
      elif item=="qc_status":
        pass
      elif item=="date":
        pass
    return render( request , "qc/list.html", { "data": p_response } )


  def post( self, request, *args, **kwargs ):
    draw = request.POST.get("draw", 1 )
    columns = request.POST.get("columns","")
    order = request.POST.get("order","")
    START = request.POST.get("start",0)
    LENGTH = request.POST.get("length",10)
    SEARCH = str(request.POST.get("search[value]",""))
    USERID = request.user.id
    Columns = []
    DSTR = ""
    obj = PagePermissions( "/qc/list", request.user.id )
    res_perm_fields = obj.get_permission_str( )

    for item in res_perm_fields:
      l = [ item["perm"], item["ctype"], item["id"] ]
      p = {}
      p[item["display_name"]] = l
      p["title"] = item["display_name"]
      DSTR = DSTR + item["table_alias"]+"."+item["id"] + ","
      Columns.append(p)
    t_data = self._formatData(DSTR.rstrip(","), SEARCH, USERID, START, LENGTH, request )
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


  def tuple_format(self, value1, value2):
    str =''
    if len(value1) == 1 and len(value2) == 1:
      str += "(property_youtube_videos.channel_id_fk_id IN ( select id from property_channel where cms_id_id IN ({0}) ) or property_youtube_videos.channel_id_fk_id IN ({1})) and ".format(value1[0], value2[0])
    elif len(value1) == 1:
      str += "(property_youtube_videos.channel_id_fk_id IN ( select id from property_channel where cms_id_id IN ({0}) ) or property_youtube_videos.channel_id_fk_id IN {1}) and ".format(value1[0], value2)
    else:
      str += "(property_youtube_videos.channel_id_fk_id IN ( select id from property_channel where cms_id_id IN {0} ) or property_youtube_videos.channel_id_fk_id IN ({1})) and ".format(value1, value2[0])
    return str


  def _formatData( self, SELECT_FIELDS, SEARCH, USERID, START, LENGTH, request ):
    filter_flag = request.POST.get('filter')
    if filter_flag:
      v = request.POST
      str = ""
      value1, value2 = tuple(filter(None,v.getlist('f_cms'))) ,tuple(filter(None,v.getlist('f_channel')))
      if ('f_cms' in v and v['f_cms']) and ('f_channel' in v and v['f_channel']):
        if len(value1) !=1 and len(value2) !=1:
           str += "(property_youtube_videos.channel_id_fk_id IN ( select id from property_channel where cms_id_id IN {0} ) or property_youtube_videos.channel_id_fk_id IN {1}) and ".format(value1, value2)
        else:
          str += self.tuple_format(value1, value2)
      elif ( 'f_channel' in v and v['f_channel'] ):
        a = "property_youtube_videos.channel_id_fk_id IN {0} and " . format( tuple(filter(None,v.getlist('f_channel')) ) )
        str += "property_youtube_videos.channel_id_fk_id IN ({0}) and " . format( tuple(filter(None,v.getlist('f_channel')) )[0] )  if len(value2)==1 else a
      elif ('f_cms' in v and v['f_cms']):
        b = "property_youtube_videos.channel_id_fk_id IN ( select id from property_channel where cms_id_id IN {0} ) and ".format( tuple(filter(None,v.getlist('f_cms'))))
        str += "property_youtube_videos.channel_id_fk_id IN ( select id from property_channel where cms_id_id IN ({0}) ) and ".format( tuple(filter(None,v.getlist('f_cms')))[0])if len(value1)== 1 else b
      for key, value in v.items():
        if (key == "f_qc_by"):
          c = "qc_qclog.qced_by_id IN {0} and " . format( tuple(filter(None,v.getlist('f_qc_by'))))
          str += "qc_qclog.qced_by_id IN ({0}) and " . format( tuple(filter(None,v.getlist('f_qc_by')))[0]) if len(tuple(filter(None,v.getlist('f_qc_by')))) == 1 else c
        elif (key == "f_daterange"):
          raw_daterange = v.get('f_daterange').split(" - ")
          str += "qced_on between '{0}'::timestamp and '{1}'::timestamp and ". format(raw_daterange[0], raw_daterange[1])
      WHERE = "property_youtube_videos.video_title like '%%{0}%%' and property_cms.is_active = True and property_channel.is_active = True and {1} " . format(SEARCH, str)
      WHERE += "True"
    else:
      WHERE = '''property_youtube_videos.video_title like '%%%s%%' and property_cms.is_active = True and property_channel.is_active = True and qc_qclog.qc_status= False and property_youtube_videos.channel_id_fk_id IN (1,2) AND property_youtube_videos.channel_id_fk_id 
        IN (select raci_yt_ch.channel_id as channel_id from raci_property_ownership_channel_name_id_fk as raci_yt_ch 
        where raci_yt_ch.property_ownership_id = (select id from raci_property_ownership where user_id_fk_id = %d) 
        union select id as channel_idB from property_channel where cms_id_id IN 
        (select cms_id_id from raci_property_ownership_channel_name_id_fk where property_ownership_id = 
        (select id as raci_po from raci_property_ownership where user_id_fk_id = %d)))''' % ( SEARCH, USERID, USERID )

    QUERY = '''SELECT %s, count(*) over() as full_count from property_youtube_videos join property_channel on property_youtube_videos.channel_id_fk_id = property_channel.id 
     join property_cms on property_channel.cms_id_id = property_cms.id join qc_qclog on qc_qclog.video_id_id = property_youtube_videos.id where %s LIMIT %d OFFSET %d''' % (SELECT_FIELDS, WHERE, int(LENGTH), int( START))
    response = self.psy._custom( QUERY.replace("\n"," ").replace("\r",""), "select", "named_tuple" )
    return response
