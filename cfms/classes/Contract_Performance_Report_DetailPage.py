import sys, json
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from libraries.PostgreSQLConnector import PostgreSQLConnector

class Contract_Performance_Report_DetailPage:

  def __init__(self, contract_id):
    self.psy = PostgreSQLConnector()
    self.contract_id = int(contract_id)

  def ContractOverallPerformanceReview(self):
    QUERY = '''select sum(ce.revenue) as total_revenue, efe.currency_from_currency, efe.currency_to_currency, (efe.currency_to * sum(ce.revenue)) as gross_earning from cfms_earning as ce join cfms_contract as cc on cc.id = ce.contract_id 
      join extras_fexchange as efe on efe.id = ce.currency_id where ce.contract_id = %d group by ce.contract_id, efe.currency_to, efe.currency_from_currency, efe.currency_to_currency''' % (self.contract_id)
    return self.psy._custom( QUERY, "select", "named_tuple")

  def CheckIfContractExists(self):
    QUERY = '''SELECT count(*) from cfms_contract where id = %d''' % ( self.contract_id )
    r = self.psy._custom(QUERY, "select")
    if len(r['data']) != 0 and r['data'][0][0] != 0:
      return True
    return False

  def ContractRightsGroup( self ):
    QUERY = '''SELECT cip.entity, cip.right_type, cip.exclusivity, cip.inclusivity from 
      cfms_iprightgroup_ip_right as ciprt join cfms_ipright as cip on cip.id = ciprt.ipright_id 
      where ciprt.iprightgroup_id = (select rights_group_id from cfms_contract where id = %d)''' % ( self.contract_id )
    return self.psy._custom(QUERY, "select","named_tuple")

  def get_date_string( self, date_str , option ):
    dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
    if option=="first_day_of_month":
      return str(dt_obj.year)+"-"+str(dt_obj.month)+"-01"
    elif option == "last_day_of_month":
      next_month = dt_obj.replace(day=28) + timedelta(days=4)
      return str(next_month - timedelta(days=next_month.day))

  def ContractSignatories( self ):
    QUERY = '''SELECT concat( ep.partner_name,' ', (ep.code)) as signatory, ccs.rev_percentage,ep.id as partner_id, 
      concat(ec.first_name,' ',ec.middle_name,' ',ec.last_name) as contact, ec.id as contact_id from cfms_contract_signatories as ccs
      join extras_partner as ep on ccs.partner_id = ep.id 
      join extras_contact as ec on ccs.contact_id = ec.id 
      where ccs.contract_id = %d  ''' % ( self.contract_id )
    return self.psy._custom(QUERY,"select","named_tuple")

  def ContractInfo( self ):
    QUERY = '''select cc.id, cc.code, cc.sign_date, cc.start_date, cc.end_date, cc.perpetual, cc.notes, 
      concat(gct.prefix,' ',gct.main_category,' ',gct.sub_category) as contract_nature, cc.contract_status 
      from cfms_contract as cc join generic_contract_type as gct on cc.nature_id = gct.id where cc.id = %d ''' % ( self.contract_id )
    return self.psy._custom(QUERY,"select","named_tuple")

  def MonthlyAggregateEarning( self ):
    QUERY = '''select TO_CHAR(ce.month, 'Mon YYYY') as month, ce.contract_id as contract_id,  sum(ce.revenue) as total_revenue,
      concat(efe.currency_from,' ',efe.currency_from_currency,' = ', efe.currency_to,' ', efe.currency_to_currency) as currency_exchange, 
      efe.currency_from_currency, efe.currency_to_currency from cfms_earning as ce join cfms_contract as cc on cc.id = ce.contract_id 
      join extras_fexchange as efe on efe.id = ce.currency_id where ce.contract_id = %d group by TO_CHAR(ce.month, 'Mon YYYY'), 
      ce.contract_id, currency_exchange, efe.currency_from_currency, efe.currency_to_currency order by month asc''' % (self.contract_id)
    return self.psy._custom(QUERY,"select","named_tuple")

  def getTableHeader(self):
    r_columns = [
      {"title": "Title Code", "data": "title_code","orderable":False, "searchable":True},
      {"title": "Title Name", "orderable":False, "data": "title_name", "searchable":True},
      {"title": "Platform Name", "orderable":False, "data": "platform_name", "searchable":True},
    ];
    QUERY = '''select ep.code from cfms_contract_signatories as ccs 
      join extras_partner as ep on ep.id = ccs.partner_id where ccs.contract_id = %d''' % (self.contract_id)
    r = self.psy._custom(QUERY, "select","named_tuple")
    for item in r["data"]:
      t = {}
      t["title"] = item.code
      t["orderable"]=False
      t["data"] = str(item.code)
      t["searchable"] = False
      r_columns.append(t)
    r_columns.append({"title":"Total Gross Earning", "orderable":False,"data":"gross_earning","searchable":False})
    return r_columns

  def get_formated_data ( self, r ):
    FINAL = []
    if( len(r['data'])!=0 ):
      for idx,item in enumerate(r['data']):
        title_code = str(item.title_code)
        Main = {}
        Node = {}

        if not any(d['title_code'] == title_code for d in FINAL):
         SNode = {}
         Node["title_code"] = item.title_code
         Node["title_name"] = item.title_name
         Node["platform_name"] = item.platform_name
         Node['gross_earning'] = item.gross_earning
         Node[str(item.partner_code)] = item.gross_earning
         FINAL.append( Node )
        else:
         offset = len(FINAL) - 1
         FINAL[offset]['gross_earning'] = FINAL[offset]['gross_earning'] + item.gross_earning
         FINAL[offset][str(item.partner_code)] = item.gross_earning
    return FINAL

  def getGivenMonthRevBreakup ( self, request):
    DRAW = request.POST.get("draw", 1 )
    START = request.POST.get("start",0)
    LENGTH = request.POST.get("length",10)
    SEARCH = str(request.POST.get("search[value]",""))
    USERID = request.user.id
    month = request.POST.get("custom_filter[for_month]","Aug 1991")
    currency_to = request.POST.get("custom_filter[converted_currency]",False)

    if currency_to == "yes":
      SUM = ', (efe.currency_to * sum(ces.calculated_revenue_usd)) as gross_earning '
      GRP = ", efe.currency_to"
    else:
      SUM = ", sum(ces.calculated_revenue_usd) as gross_earning"
      GRP = ""

    QUERY = '''SELECT at.code as title_code, at.display_name as title_name, ep.code as partner_code, gp.platform_name %s from cfms_earningsplit as ces
      join cfms_earning as ce on ce.id = ces.earning_ref_id join extras_partner as ep on ep.id = ces.partner_id
      join generic_platform as gp on gp.plat_id = ce.platform_id_id join extras_fexchange as efe on efe.id = ce.currency_id
      join asset_title as at on at.id = ce.title_id_id join cfms_contract as cc on cc.id = ce.contract_id
      where (at.code like '%%%s%%' or at.display_name like '%%%s%%') and  ce.contract_id = %d and TO_CHAR(ce.month, 'Mon YYYY') LIKE '%s'
      group by at.code, at.display_name , ep.code, ce.month, gp.platform_name %s LIMIT %d OFFSET %d''' % ( str(SUM), str(SEARCH), str(SEARCH), self.contract_id, str(month), str(GRP), int(LENGTH), int(START) )
    r = self.psy._custom( QUERY, "select","named_tuple" )
    FINAL = self.get_formated_data( r )
    return {"data":FINAL, "draw":DRAW, "recordsTotal":r['count'],"recordsFiltered":r['count']}


