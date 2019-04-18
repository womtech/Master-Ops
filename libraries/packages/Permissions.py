import psycopg2, sys, json
sys.path.insert(0,'/projects/mops')
from libraries import PostgreSQLConnector as psql

class PagePermissions:

  def __init__(self, context_url, user_id):
    self.context_url = context_url
    self.user_id = user_id
    self.raw_perm = []
    self.psql = psql.PostgreSQLConnector()
    self.raci = {
      "cms": {'table':'raci_property_ownership_cms_name_id_fk','column':'cms_id','jtbl':'property_cms'},
      "channel": {'table':'raci_property_ownership_channel_name_id_fk','column':'channel_id','jtbl':'property_channel'},
      "contract": {'table':'raci_property_ownership_contract_id_fk','column':'contract_id','jtbl':'cfms_contract'},
      "facebook": {'table':'raci_property_ownership_facebook_page_id_fk','column':'facebook_id','jtbl':'property_facebook'},
      "instagram": {'table':'raci_property_ownership_instagram_account_name_id_fk','column':'instagram_id','jtbl':'property_instagram'},
      "twitter": {'table':'raci_property_ownership_twitter_account_name_id_fk','column':'twitter_id', 'jtbl':'property_twitter'}
    }
    self.execute(  )


  def is_page_permitted( self  ):
    QUERY = '''select count(id) as is_present from system_user_form_level_permission where form_id_fk_id IN
     (select id from system_app_form where form_name_html ~ '%s') AND app_assignment_id_fk_id IN
     (select id from system_apps_assignment where user_id_fk_id = %d )''' % ( self.context_url, self.user_id )
    r = self.psql._custom( QUERY , "select")
    if len(r['data']) != 0 and r['data'][0][0] != 0:
      return True
    return False

  def execute( self ):
    QUERY = '''select sa.filter, sa.available_operations, sa.permission_str, sa.search, sa.form_type, sa.full_privilege_on from system_apps_assignment saa join system_user_form_level_permission sa \
      on saa.id=sa.app_assignment_id_fk_id where saa.user_id_fk_id = %d and sa.form_url = '%s' ''' % ( self.user_id, self.context_url )
    self.raw_perm = self.psql._custom( QUERY, "select","named_tuple")

  def get_filter( self ):
    return self.raw_perm['data'][0][0]

  def get_available_operations( self ):
    return self.raw_perm['data'][0][1]

  def get_permission_str( self ):
    return self.raw_perm['data'][0][2]

  def get_search_fields( self ):
    return self.raw_perm['data'][0][3]

  def get_view_type( self ):
    return self.raw_perm['data'][0][4]

  def get_privilege_type( self ):
    return self.raw_perm['data'][0][5]

  def check_raci( self, raci_type, property_id ):
    fp_status = self.get_privilege_type()
    if fp_status:
      return True
    QUERY = '''select count(*) from %s as a where a.property_ownership_id =
      (select id from raci_property_ownership where user_id_fk_id = %d) 
      and a.%s = %d''' %  ( self.raci[raci_type]["table"],self.user_id, self.raci[raci_type]["column"], int(property_id) )
    r = self.psql._custom( QUERY, "select")
    if len(r['data']) != 0 and r['data'][0][0] != 0:
      return True
    return False


  def get_raci( self, raci_type ):
    fp_status = self.get_privilege_type()
    status = "b.is_active"
    if raci_type == "contract":
      status = True

    if fp_status:
      QUERY = '''select a.* from %s as a where %s''' % (self.raci[raci_type]["jtbl"], status )
    else:
      QUERY = '''select b.* from %s as a join %s as b on a.%s = b.id where a.property_ownership_id =
        (select id from raci_property_ownership where user_id_fk_id = %d) and %s
      ''' % ( self.raci[raci_type]["table"], self.raci[raci_type]["jtbl"], self.raci[raci_type]["column"], self.user_id, status )
    r = self.psql._custom( QUERY , "select","named_tuple")
    if len(r['data']) == 0:
      return False
    return r["data"]

