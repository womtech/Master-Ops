from django.contrib import admin
from .models import Contract, Contract_Signatories, Earning, EarningSplit, Distribution, IPRight, IPRightGroup

class ContractAdmin( admin.ModelAdmin ):
  search_fields = ('code','contract_status')
  list_display = ('code','sign_date','start_date','end_date','perpetual','notes','attach', 'contract_status')
  list_filter = ('code','contract_status')

class Contract_SignatoriesAdmin( admin.ModelAdmin ):
  search_fields = ('signer','partner')
  list_display = ('code','partner','contract','rev_percentage','contact','signer')
  list_filter = ('contract','partner')

class EarningAdmin( admin.ModelAdmin ):
  list_display = ('code','month','currency','revenue','contract','platform_id')
  list_filter = ('platform_id','contract')
  search_fields = ('code',)

class EarningSplitAdmin( admin.ModelAdmin ):
  list_display=('code','calculated_revenue_usd','partner','earning_ref')
  list_filter = ('partner',)

class DistributionAdmin( admin.ModelAdmin ):
  list_display = ('code','contract','platform','title')
  list_filter = ('platform', 'distributed_on')

admin.site.register( Contract, ContractAdmin )
admin.site.register( Contract_Signatories, Contract_SignatoriesAdmin )
admin.site.register( Earning, EarningAdmin )
admin.site.register( EarningSplit, EarningSplitAdmin )
admin.site.register( Distribution, DistributionAdmin )
admin.site.register(IPRight)
admin.site.register(IPRightGroup)
