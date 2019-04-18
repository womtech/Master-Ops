from import_export import resources
from .models import Hcpc, TrendingKeywords

class HcpcResource(resources.ModelResource):
  class Meta:
    model   = Hcpc
    exclude = ('id',)
    skip_unchanged 	 = True
    report_skipped	 = True
    import_id_fields     = ('keyword',)
    fields = ('keyword', 'volume', 'keyword_difficulty', 'cost_per_click', 'competitive_density', 
		     	  'results', 'serp_features', 'date')

class TrKeywordsResource(resources.ModelResource):
  class Meta:
    model   = TrendingKeywords
    exclude = ('id',)
    skip_unchanged	 = True
    report_skipped	 = True
    import_id_fields     = ('keyword',)
    fields = ('keyword', 'volume', 'keyword_difficulty', 'cost_per_click', 'competitive_density', 
		      	  'results', 'serp_features', 'date')

