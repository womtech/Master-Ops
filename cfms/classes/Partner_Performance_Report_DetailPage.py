import sys, json
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
from libraries.PostgreSQLConnector import PostgreSQLConnector

class Partner_Performance_Report_DetailPage:

  def __init__(self, partner_id):
    self.psy = PostgreSQLConnector()
    self.partner_id = int(partner_id)

  def getPartnerBasicInfo( self ):
    QUERY = '''select * from extras_partner where id = %d''' % (self.partner_id)
    return self.psy._custom(QUERY,"select","named_tuple")

  def getPartnerContracts( self ):
    QUERY = '''select ccs.rev_percentage, ccs.signer, cc.id as contract_id, cc.code, cc.contract_status, 
      concat(gct.prefix,'-',gct.main_category,'/',gct.sub_category) as contract_type, cc.sign_date, cc.start_date, 
      cc.end_date, cc.perpetual, ec.id as contact_id, ec.official_name, ec.primary_contact as contact_m_pri, 
      ec.secondary_contact as contact_m_sec, ec.primary_email as contact_e_pri, ec.secondary_email as contact_e_sec, ec.code as contact_code, 
      gat.name as contact_association_name from cfms_contract_signatories as ccs 
      join cfms_contract as cc on cc.id = ccs.contract_id 
      join extras_contact as ec on ec.id = ccs.contact_id 
      join generic_contract_type as gct on gct.id = cc.nature_id 
      join generic_association_type as gat on gat.id = ec.contact_type_id where partner_id = %d''' % (self.partner_id)
    return self.psy._custom(QUERY,"select","named_tuple")

