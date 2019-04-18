from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from kpt.resources import HcpcResource, TrKeywordsResource
from .models import Hcpc, TrendingKeywords
# Register your models here.
#admin.site.register([Hcpc,TrendingKeywords])


class HcpcsAdmin( admin.ModelAdmin ):
  search_fields = ('keyword','volume','keyword_difficulty','cost_per_click')
  list_display = ('keyword','volume','keyword_difficulty','cost_per_click','competitive_density','results','serp_features','date')
  list_filter = ('keyword','volume')


class TrendingKeywordsAdmin( admin.ModelAdmin ):
  search_fields = ('keyword','volume','keyword_difficulty')
  list_display = ('keyword','volume','keyword_difficulty','cost_per_click','competitive_density','results','serp_features','date')
  list_filter = ('keyword','cost_per_click')

admin.site.register( TrendingKeywords, TrendingKeywordsAdmin )
admin.site.register( Hcpc, HcpcsAdmin )

class HcpcAdmin(ImportExportModelAdmin):
  resource_class = HcpcResource
  fields         = ('keyword', 'volume', 'keyword_difficulty', 'cost_per_click', 'competitive_density',
		              'results', 'serp_features', 'date')

class TKeywordsAdmin(ImportExportModelAdmin):
  resource_class = TrKeywordsResource
  fields = ('keyword', 'volume', 'keyword_difficulty', 'cost_per_click', 'competitive_density',
		      'results', 'serp_features', 'date')
