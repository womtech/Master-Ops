from django.contrib import admin
from asset.models import Title, Album

# Register your models here.

class TitleAdmin( admin.ModelAdmin ):
  search_fields = ('display_name','isrc_code')
  list_display = ('code','display_name','type','genre','language','acquisition_cost','release_year','deep_link')
  list_filter = ('type','language','genre','status')

class AlbumAdmin( admin.ModelAdmin ):
  search_fields = ('album_name','upc_code','genre',)
  list_display = ('upc_code','album_name','description','genre','release_date',)
  list_filter = ('genre','release_date')

admin.site.register( Title, TitleAdmin )
admin.site.register( Album, AlbumAdmin )
