from django.contrib import admin
from .models import qclog


class qclogAdmin( admin.ModelAdmin ):
  search_fields = ('qced_by','qc_status')
  list_display = ('id','moderator_remark','qced_by','qced_on','qc_status')
  list_filter = ('qced_by','qc_status')

admin.site.register( qclog, qclogAdmin )
