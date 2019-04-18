from django.contrib import admin
from .models import Contact, Partner, FExchange

# Register your models here.

class ContactAdmin( admin.ModelAdmin ):
  search_fields = ('primary_email','official_name')
  list_display = ('code','first_name','middle_name','last_name','official_name','primary_contact','primary_email')
  list_filter = ('contact_type','code','primary_email','official_name')

class PartnerAdmin( admin.ModelAdmin ):
  search_fields = ('partner_name','custom_id','genre')
  list_display = ('code','partner_name','email','phone','website','custom_id')
  list_filter = ('poc','code')

class FExchangeAdmin( admin.ModelAdmin ):
  search_fields = ('code',)
  list_display = ('code','date','currency_from','currency_to','added_on')
  list_filter = ('date','code')

admin.site.register( Contact, ContactAdmin )
admin.site.register( Partner, PartnerAdmin )
admin.site.register( FExchange, FExchangeAdmin )
